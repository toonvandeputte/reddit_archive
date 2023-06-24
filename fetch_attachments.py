import requests
import os
import glob
import json
from http import cookiejar 
from slugify import slugify

class BlockAll(cookiejar.CookiePolicy):
	return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
	netscape = True
	rfc2965 = hide_cookie2 = False

def walk_dir(dir):
	for name in glob.glob(dir+'/*'):
		if os.path.isdir(name):
			walk_dir(name)
		else:
			extract_attachments(name)

def extract_attachments(fpath):
	# print(fpath)
	if fpath.endswith('.json'):
		# print('is json')
		dir = fpath[:-5]
		with open(fpath,'r') as f:
			obj = json.load(f)
			if 'url' in obj:
				maybe_download_file(obj['url'],dir)
			if 'post' in obj:
				if 'url' in obj['post']:
					maybe_download_file(obj['post']['url'],dir)

def maybe_download_file(url,dir):
	if '' == url:
		return
	# return True
	if 'www.reddit.com/gallery' in url:
		print('gallery: '+url)
		download_gallery(url,dir)
		return
	extensions = ['.jpg','.png','.zip','.pdf','.gif','.mp4', '.gifv']
	fname = os.path.basename(url)
	lastpart = fname[-8:]
	ext = lastpart.split('.')
	if 1 == len(ext):
		if url.startswith('/r/'):
			url = f"https://www.reddit.com{url}"
		if url.startswith('http'):
			print("fetching: "+url)
			try:
				f = requests.get(url)
			except:
				print("fetch failed, unreachable?")
				return
			ctype = f.headers['Content-Type']
			print('ctype: ' + ctype)
			if not ctype.startswith('image'):
				return
			pext = ctype.split('/')[-1]
			if '*' == pext:
				pext = 'unknown'
			fname = slugify(fname)[:70] + '.' + pext
			print(fname)
		else:
			return
	if len(ext) > 1:
		if f".{ext[1]}" not in extensions:
			return
			print(url)
		print(url)
	if not os.path.isdir(dir):
		os.makedirs(dir)
	fpath =  dir + '/' + fname
	print(fpath)
	if not os.path.isfile(fpath):
		with open( fpath, 'wb') as f:
			f.write(requests.get(url).content)

def download_gallery(url,dir):
	pathcomps = url.split('gallery/')
	gallery_id = pathcomps[-1]
	json_url = f"https://www.reddit.com/comments/{gallery_id}.json"
	s = requests.Session()
	headers = {
		'User-Agent': 'My User Agent 1.0'
	}
	s.cookies.clear()
	s.cookies.set_policy(BlockAll())
	gallery = s.get(json_url,headers=headers)
	assert not s.cookies
	galobj = gallery.json()
	galdir = dir + '/gallery/'+gallery_id
	if not os.path.isdir(galdir):
		os.makedirs(galdir)
	with open( galdir + '/gallery.json', 'w') as f:
		json.dump(gallery.json(),f)
	for i in galobj:
		for c in i['data']['children']:
			if 'is_gallery' in c['data'] and True == c['data']['is_gallery']:
				imgs = []
				if 'media_metadata' in c['data'] and c['data']['media_metadata'] != None:
					for k, v in c['data']['media_metadata'].items():
						imgs.append([k,v['m']])

				for i in imgs:
					ext = i[1].split('/')[1]
					imgurl = f"https://i.redd.it/{i[0]}.{ext}"
					maybe_download_file(imgurl,galdir)

def run():
	walk_dir('output')

if '__main__' == __name__:
	run()
import praw
import json
import os
from slugify import slugify
from datetime import date

secrets = {}
reddit = None

def get_secrets():
	global secrets
	if not secrets:
		with open('credentials.json','r') as sf:
			return json.load(sf)
	return secrets

def get_reddit():
	global reddit
	if None == reddit:
		s = get_secrets()
		reddit = praw.Reddit(
			client_id=s['client_id'],
			client_secret=s['client_secret'],
			password=s['pass'],
			username=s['username'],
			user_agent="AutomatonBe/0.0.1",
		)
	return reddit

def fetch_submissions():
	reddit = get_reddit()
	s = get_secrets()
	user = reddit.redditor(s['username'])
	submissions = user.submissions.new(limit=None)
	odir = 'output/submissions'
	if not os.path.isdir(odir):
		os.makedirs(odir)
	for sub in submissions:
		store_submission(sub,odir)

def store_submission(sub,dir):
	ts = date.fromtimestamp(sub.created_utc).isoformat()
	fname = slugify(f"{ts}-{sub.title[:70]}-{sub.id}")
	sr =  sub.subreddit
	# print(sr.display_name)
	# continue
	obj = {
		'id' : sub.id,
		'name' : sub.name,
		'date' : ts,
		'utc' : sub.created_utc,
		'title' : sub.title,
		'text' : sub.selftext,
		'permalink' : sub.permalink,
		'subreddit' : sr.display_name,
		'score' : sub.score,
		'url' : sub.url
	}
	srdir = dir + '/' + sr.display_name
	# dirname = slugify(str(sub.created_utc)+'-'+sub.title+'-'+sub.id)
	# print(srdir)
	if not os.path.isdir(srdir):
		os.makedirs(srdir)
	with open(srdir + '/' + fname + '.json', 'w') as of:
		json.dump(obj, of, indent=4)
	if sub.selftext:
		with open(srdir + '/' + fname + '.md', 'w') as of:
			of.write(f"#{sub.title}\n\n{sub.selftext}")

def store_comment(com,dir):
	ts = date.fromtimestamp(com.created_utc).isoformat()
	fname = slugify(f"{ts}-{com.id}")
	sr =  com.subreddit
	sub =  com.submission
	obj = {
		'id' : com.id,
		'parent_id' : com.parent_id,
		'name' : com.name,
		'date' : ts,
		'utc' : com.created_utc,
		'text' : com.body,
		'permalink' : com.permalink,
		'post' : {
			'id' : sub.id,
			'title' : sub.title,
			'subreddit' : sr.display_name,
			'text' : sub.selftext,
			'url' : sub.url
		},
		'score' : com.score
	}
	srdir = dir + '/' + sr.display_name
	if not os.path.isdir(srdir):
		os.makedirs(srdir)
	with open(srdir + '/' + fname + '.json', 'w') as of:
		json.dump(obj, of, indent=4)
	with open(srdir + '/' + fname + '.md', 'w') as of:
		of.write(com.body)

def fetch_saved():
	reddit = get_reddit()
	s = get_secrets()
	user = reddit.redditor(s['username'])
	saved = user.saved(limit=None)
	odir = 'output/saved'
	if not os.path.isdir(odir):
		os.makedirs(odir)
	for sav in saved:
		# print(type(sav))
		if hasattr(sav,'body'):
			store_comment(sav,odir+'/comments')
			# print('comment')
		else:
			store_submission(sav,odir+'/posts')
			# print('submission')
		# store_submission(sub,odir)

def run():
	fetch_saved()
	fetch_submissions()

	# print(self_texts)


if '__main__' == __name__:
	run()
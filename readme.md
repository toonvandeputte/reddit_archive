# Archive your Reddit content

This Python (3.11) script creates a local archive of:

- Your own Reddit posts (*not* comments)
- The Reddit content you saved (posts and comments)
- Attachments (images) belonging to that content

## Reddit credentials

In order for this script to work, you need to create a `credentials.json` file with your Reddit API credentials and your Reddit username and password.

You can get Reddit API credentials by creating a Reddit app on [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps). 

## Python virtual environment

You don't *need* a Python virtual environment, but it is the most convenient way to run the script. In order to create one, run:

`python -m venv _venv --upgrade-deps`, as described on [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html). Then you can enter the virtual environment with `source _venv/bin/activate`. Subsequently, installing the required packages can be done with `pip install -R requirements.txt`.

## Running the scripts

There are two separate `.py` files included. The main one to use is `reddit_archive.py`. This will download all your posts, and all the comments and posts you haved saved in the `output` directory. Your own content will be in `output/posts` and the saved content will be in `output/saved`. Everything will be organized by subreddit and date.

Once this script has completed (it can take quite a while, depending on how much content there is), you can download any attached images with `fetch_attachments.py`. This will check the `url` properties of posts, determine whether they contain image links and download those images. Galleries will also be downloaded, although I have noticed that this doesn't always work and sometimes a placeholder images instead of the real one will be downloaded. This might be some hotlinking protection at work.

If you run `fetch_attachments.py` more than once, images that already exist will not be overwritten, to prevent unneeded downloads. So if you want to force the download of images, you will have to manually delete the previously downloaded version.
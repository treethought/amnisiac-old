import praw
import requests
from bs4 import BeautifulSoup as bs
from markdown import markdown
import os

from project.server.scrapers.video_ids import get_video_id

#script
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     # password='password', # not needed for read only
                     user_agent='testscript by /u/squeeney',
                     username='squeeney')


def hot_posts(sub):
    result = []
    print('fetchin {} subreddit'.format(sub))
    try:
        for post in reddit.subreddit(sub).hot():
            if post.media:
                post.video_id = get_video_id(post.domain, post.url)
                result.append(post)

    except praw.exceptions.PRAWException as e:
        print('No subreddit found for {}'.format(sub))
    return result


def get_audio(post_url):
    if 'youtube' in post_url:
        pass


def wiki_subs(sub, wiki_name):
    wiki = reddit.subreddit(sub).wiki[wiki_name]
    html = markdown(wiki.content_md)
    subs = bs(html, 'html.parser').select('li')
    sub_names = []
    for sub in subs:
        if '/r/' in sub.text[:3]:
            name = sub.text.strip('/r/').split()[0]
            sub_names.append(name)
    return sub_names


def split_by_domain(submissions):
    domains = {'youtube': [], 'vimeo': []}
    yt_posts = [p for p in submissions if 'you' in p.domain]
    for p in [p for p in yt_posts if p.video_id]:
        if len(p.video_id) == 11:  # ensure id is valid 11-char
            domains['youtube'].append(p)

    domains['vimeo'] = [p for p in submissions if 'vim' in p.domain]

    return domains






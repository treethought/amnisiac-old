# project/server/reddit/api.py

import os
from markdown import markdown
import praw
from bs4 import BeautifulSoup as bs


from project.server.reddit.video_ids import get_video_id

# Type Annotations #
from typing import List, Iterable
from praw.models import Submission

# script
reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                     client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                     # password='password', # not needed for read only
                     user_agent='testscript',
                     username=os.getenv('REDDIT_USERNAME'))


def fetch_submissions(subreddits: List[str]) -> List[Submission]:
    sub_query = ''
    for sub in subreddits:
        sub_query += sub.strip(',').strip('/r/') + '+'
    return hot_posts(sub_query)


def build_sources() -> List[tuple]:
    subs = wiki_subs('music', 'musicsubreddits')
    sub_names = []
    for s in subs:
        name = '/r/{}'.format(s)
        choice = (name, name)
        sub_names.append(choice)  # choices must be tuples
    return sub_names


def hot_posts(sub: str) -> List[Submission]:
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


def wiki_subs(sub: str, wiki_name: str) -> Iterable[str]:
    wiki = reddit.subreddit(sub).wiki[wiki_name]
    html = markdown(wiki.content_md)
    subs = bs(html, 'html.parser').select('li')
    for sub in subs:
        if '/r/' in sub.text[:3]:
            name = sub.text.strip('/r/').split()[0]
            yield name


def split_by_domain(submissions):
    domains = {'youtube': [], 'vimeo': []}
    yt_posts = [p for p in submissions if 'you' in p.domain and p.video_id]
    for p in yt_posts:
        if len(p.video_id) == 11:  # ensure id is valid 11-char
            domains['youtube'].append(p)

    domains['vimeo'] = [p for p in submissions if 'vim' in p.domain]

    return domains

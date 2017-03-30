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
                # print(post.video_id)
    except praw.exceptions.PRAWException as e:
        print('No subreddit found for {}'.format(sub))
        print(e)
    return result
        # yield submission.title

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


        


# def wiki_subs(subreddit, wiki_name):
#     # subs = []
#     # wiki_url = 'https://www.reddit.com/r/{}/wiki/{}'.format(subreddit, wiki_name)
#     # resp = requests.get(wiki_url)
#     # resp.raise_for_status
#     print(resp.status_code)
#     soup = bs(resp.content, 'html.parser')
#     items = soup.select('li > a')
#     with open('music_subs.txt', 'w+') as f:
#         for i in items:
#             url = i.get('href')
#             if '/r/' in url[:3]:
#                 sub_name = url.strip('/r/')
#                 subs.append(sub_name)
#                 f.write(sub_name+'\n')


    # print(subs)
    # return subs

def st():
    for submission in reddit.subreddit('news').stream.submissions():
        print(submission)



if __name__ == '__main__':
    # wiki_subs('music', 'musicsubreddits')
    st()




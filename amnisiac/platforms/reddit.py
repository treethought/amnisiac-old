# amnisiac/platforms/reddit.py
import os
from markdown import markdown
import praw
from bs4 import BeautifulSoup as bs


from amnisiac.platforms.utils import get_video_id


reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                     client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                     # password='password', # not needed for read only
                     user_agent='testscript',
                     username=os.getenv('REDDIT_USERNAME'))


def fetch_submissions(subreddits):
    """Returns list of hot submissions for the given subreddits

    Arguments:
        subreddits {str} -- reddit style query ex. jazz+listent

    Returns:
        list -- list of submission items
    """
    sub_query = ''
    for sub in subreddits:
        sub_query += sub.strip(',').strip('/r/').strip('+') + '+'
    return hot_posts(sub_query)


def build_sources():
    subs = wiki_subs('music', 'musicsubreddits')
    sub_names = []
    for s in subs:
        name = '/r/{}'.format(s)
        choice = (name, name)
        sub_names.append(choice)  # choices must be tuples
    return sub_names


def hot_posts(sub):
    """Returns modified 'hot' submissions that contain media

    Submissions with the media attribute are assigned a video_id attribute

    Arguments:
        sub {str} -- name of subreddit

    Returns:
        list -- list of submission objects with youtube video_id attribute

    Raises:
        e -- [description]
    """
    result = []
    print('fetchin {} subreddit'.format(sub))

    if sub == '+':
        return []

    try:
        for post in reddit.subreddit(sub).hot():
            if post.media:
                post.video_id = get_video_id(post.domain, post.url)
                result.append(post)

    except praw.exceptions.ClientException as e:
        raise e
    except praw.exceptions.APIException as e:
        print(e)

    except praw.exceptions.PRAWException as e:
        print('No subreddit found for {}'.format(sub))

    except Exception as e:
        print(e)
        print('sub query: {}'.format(sub))

    return result


def wiki_subs(sub, wiki_name):
    """Returns the names of subreddits incldued in a sub's wiki markdown"""

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

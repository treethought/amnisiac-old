import itertools

from project.server import db
from project.server.models import Item, get_or_create


def item_from_reddit(submission):
    """Submission requires video_id, added to object inside hot_posts"""

    item = get_or_create(
        db.session, Item, track_id=submission.video_id, source='reddit')
    item.subreddit = submission.subreddit_name_prefixed
    item.url = submission.url
    item.domain = submission.domain
    item.raw_title = submission.title

    return item


def item_from_sc(resource):

    item = get_or_create(db.session, Item, track_id=str(resource.id), source='sc')
    item.artist = resource.user['username']
    item.title = resource.title
    item.raw_title = '{} - {}'.format(resource.user['username'], resource.title)
    item.source = 'sc'
    item.url = resource.permalink_url
    return item

def generate_items(reddit_posts, sc_tracks):
    items, reddit_items, sc_items = [], [], []

    # only doing yt, bc video_id will be '' for non-yt domains
    # used to check for yt domain in feed.html, but filtering here now
    # passing 'id' to template as item.track_id now, not video_id

    for post in reddit_posts:
        if 'you' in post.domain and post.video_id:
            item = item_from_reddit(post)
            reddit_items.append(item)

    for track in sc_tracks:
        item = item_from_sc(track)
        sc_items.append(item)

    for i in list(itertools.zip_longest(reddit_items, sc_items)):
        items.extend(i)

    return items  # TODO: refactor into generator

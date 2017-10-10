# amnisiac/platforms/utils.py
import itertools
from urllib.parse import urlparse, parse_qs
import arrow

from amnisiac.extensions import db
from amnisiac.models import Item, get_or_create


def item_from_reddit(submission):
    """Submission requires video_id, added to object inside hot_posts"""
    item = get_or_create(
        db.session, Item, track_id=submission.video_id, source='reddit')
    item.subreddit = submission.subreddit_name_prefixed
    item.url = submission.url
    item.domain = submission.domain
    item.raw_title = submission.title
    item.r_created_utc = submission.created_utc
    item.pub_date = arrow.get(submission.created_utc).timestamp
    db.session.add(item)
    db.session.commit()
    return item


def item_from_sc(resource):

    item = get_or_create(db.session, Item, track_id=str(resource.id), source='sc')

    item.artist = resource.user['username']
    item.title = resource.title
    item.raw_title = '{} - {}'.format(resource.user['username'], resource.title)
    item.source = 'sc'
    item.url = resource.permalink_url
    item.domain = 'soundcloud.com'
    item.uri = resource.uri
    item.duration = resource.duration
    item.embeddable_by = resource.embeddable_by
    item.artwork_url = resource.artwork_url
    item.streamable = resource.streamable
    item.created_at = resource.created_at
    item.pub_date = arrow.get(resource.created_at, 'YYYY/MM/DD HH:mm:ss').timestamp
    item.genre = resource.genre
    item.waveform_url = resource.waveform_url
    item.stream_url = resource.stream_url
    db.session.add(item)
    db.session.commit()
    return item


def generate_items(reddit_posts=None, sc_tracks=None):
    items = []

    for i in reddit_posts:
        if 'you' in i.domain and i.video_id:
            item = item_from_reddit(i)
            items.append(item)

    for i in sc_tracks:
        print('from sc')
        item = item_from_sc(i)
        items.append(item)

    items = filter(None, items)
    return sorted(items, key=lambda item: item.pub_date, reverse=True)


def get_video_id(domain, url):
    if 'vimeo' in domain:
        return vimeo_id(url)
    elif 'you' in domain:
        return youtube_id(url)
    elif 'soundcloud' in domain:
        # return soundcloud_id(url)
        pass # TODO
    else:
        return ''



def vimeo_id(url):
    return urlparse(url).path.lstrip("/")


# initial version: http://stackoverflow.com/a/7936523/617185
# by Mikhail Kashkin(http://stackoverflow.com/users/85739/mikhail-kashkin)
def youtube_id(url):
    """Returns Video_ID extracting from the given url of Youtube

    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',

      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]

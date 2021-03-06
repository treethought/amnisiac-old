# amnisiac/platforms/sc.py
import os
import soundcloud


client = soundcloud.Client(
    client_id=os.getenv('SOUNDCLOUD_CLIENT_ID'),
    client_secret=os.getenv('SOUNDCLOUD_CLIENT_ID'))


def get_user(name):
    for user in search_user(name):
        if user.username.lower().strip() == name.lower().strip():
            return user


def user_tracks(user, limit=None):
    try:
        endpoint = '/users/{}/tracks'.format(user.id)
        for track in client.get(endpoint, limit=5):
            yield track
    except AttributeError:
        print('No id found for {}'.format(user))
        return []


def fetch_tracks(artists):
    """ Generator yielding the internal dicts of track resources """
    tracks = []
    for q in [q for q in artists if len(q) > 1]:
        artist = get_user(q.strip())
        for track in user_tracks(artist):
            tracks.append(track)
    return tracks


def search_user(name):
    """Generator yielding Resource objects from search results"""
    results = client.get('/users', q=name, limit=10)
    for a in results:
        yield a


def embed_info(url):
    return client.get('/oembed', url=url).html


def my_stream():
    endpoint = '/me/activities/tracks/affiliated'
    for track in client.get(endpoint):
        yield track

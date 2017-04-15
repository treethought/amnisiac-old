# project/server/sc/api.py

import os
import soundcloud


# type annotations
from typing import Iterable, List, Dict
from soundcloud.resource import Resource


client = soundcloud.Client(
    client_id=os.getenv('SOUNDCLOUD_CLIENT_ID'),
    client_secret=os.getenv('SOUNDCLOUD_CLIENT_ID'))


def fetch_tracks(artists: List[str]) ->Iterable[Dict]:
    """ Generator yielding the internal dicts of track resources """
    for q in [q for q in artists if len(q) > 1]:
        artist = get_user(q.strip())
        for track in user_tracks(artist):
            track_data = {'id': track.id, 'title': track.title, 'stream': track.stream_url}
            yield track

def search_user(name: str) -> Iterable[Resource]:
    """Generator yielding Resource objects from search results"""
    results = client.get('/users', q=name, limit=10)
    for a in results:
        yield a


def get_user(name: str) -> Resource:
    for user in search_user(name):
        if user.username.lower().strip() == name.lower().strip():
            return user


def user_tracks(user: Resource, limit=None) -> Iterable[Resource]:
    try:
        endpoint = '/users/{}/tracks'.format(user.id)
        for track in client.get(endpoint):
            yield track
    except AttributeError as e:
        print('No id found for {}'.format(user))
        return []


def embed_info(url: str) -> str:
    return client.get('/oembed', url=url).html


def my_stream():
    endpoint = '/me/activities/tracks/affiliated'
    for track in client.get(endpoint):
        yield track

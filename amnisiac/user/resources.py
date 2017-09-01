from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from amnisiac.extensions import db
# from amnisiac.sources import sc

from amnisiac.models import Item, get_or_create, User, Feed

user_blueprint = Blueprint('user', __name__, url_prefix='/users')
api = Api(user_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('reddit_query')
parser.add_argument('sc_query')


item_fields = {
    # 'id': fields.Integer,
    'track_id': fields.String,
    'raw_title': fields.String,
    'title': fields.String,
    'artist': fields.String,
    'url': fields.String,
    'domain': fields.String,
    # 'date_published': fields.DateTime,
    'date_saved': fields.DateTime,
    'source': fields.String,
    'subreddit': fields.String
}

feed_fields = {
    'name': fields.String,
    'url': fields.String,
    'domain': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'feeds': fields.List(fields.Nested(feed_fields)),
    'favorites': fields.List(fields.Nested(item_fields))
}


def user_from_identity():
    """Returns the User model object of the current jwt identity"""
    username = get_jwt_identity()
    return User.query.filter(User.username == username).scalar()


class ProtectedResource(Resource):
    method_decorators = [jwt_required]


class UserResource(ProtectedResource):
    @marshal_with(user_fields)
    def get(self):
        # jwt_extended requires json serializable identity
        # so need to perform query from username
        return user_from_identity()


class Source(ProtectedResource):
    """ Add or remove sources from current user"""

    @marshal_with(user_fields)
    def post(self):
        user = user_from_identity()
        args = request.get_json()['params']
        reddit_query = args.get('reddit_query') or ''
        # sc_query = args.get('sc_query') or ''

        subreddits = reddit_query.split('+')
        # sc_artists = sc_query.split('+')

        for source in filter(None, subreddits):
            source_name = '/r/{}'.format(source)
            name, url = source_name, 'http://reddit.com' + source_name
            feed = get_or_create(db.session, Feed, name=name,
                                 url=url, domain='reddit')
            if feed not in user.feeds:
                print('adding {} to user feeds'.format(feed.name))
                user.feeds.append(feed)

        # for source in filter(None, sc_artists):
        #     artist = sc.get_user(source)
        #     name, url = source, artist.permalink_url
        #     feed = get_or_create(
        #         db.session, Feed, name=name, url=url, domain='sc')
        #     if feed not in user.feeds:
        #         user.feeds.append(feed)

        db.session.add(user)
        db.session.commit()
        return user

    @marshal_with(user_fields)
    def put(self):
        user = user_from_identity()
        args = request.get_json()['params']
        source_name = args.get('source')
        current_feeds = user.feeds
        if source_name:
            source = get_or_create(db.session, Feed, name=source_name)
            try:
                current_feeds.remove(source)
            except ValueError:
                raise  # or scream: thing not in some_list!
            except AttributeError:
                raise  # call security, some_list not quacking like a list!

        user.feeds = current_feeds
        db.session.add(user)
        db.session.commit()
        return user


class Favorite(ProtectedResource):
    """Add or remove item from favorites favorites"""

    def parse_item(self, item_json):
        """Returns an Item object using the track id and source"""
        track_id, source = item_json['track_id'], item_json['source']
        return get_or_create(db.session, Item, track_id=track_id, source=source)

    @marshal_with(user_fields)
    def put(self):
        """Remove item from favorites and return the updated User object"""

        user = user_from_identity()
        item_json = request.get_json()['item']
        item = self.parse_item(item_json)
        if item in user.favorites:
            user.favorites.remove(item)
            # db.session.add(item)
            # db.session.add(user) # user and item already in session?
            db.session.commit()
        return user_from_identity()

    @marshal_with(user_fields)
    def post(self):
        """Save item to favorites and return the updated User object"""
        item_json = request.get_json()['item']
        item = self.parse_item(item_json)

        # seperate bc info may change with post and source
        # and track_id is the real identifier
        item.raw_title = item_json['raw_title']
        item.domain = item_json['domain']
        item.url = item_json['url']
        user = user_from_identity()
        user.favorites.append(item)
        # db.session.add(item)
        db.session.merge(user)
        db.session.commit()

        # if item not in user.favorites:
        #     print('item not found, adding')
        #     user.favorites.append(item)
        #     db.session.add(item)
        #     db.session.add(user)
        #     db.session.commit()
        # else:
        #     print('item already in favorites')

        return user


api.add_resource(UserResource, '')
api.add_resource(Favorite, '/favorites')
api.add_resource(Source, '/sources')

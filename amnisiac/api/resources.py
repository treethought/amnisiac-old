from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


from amnisiac.extensions import db, bcrypt
from amnisiac.sources import reddit, sc
from amnisiac.sources.utilities import generate_items
from amnisiac.models import Item, get_or_create, User

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

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

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class RedditSources(Resource):
    def get(self):
        sub_names = []
        subs = reddit.wiki_subs('music', 'musicsubreddits')
        for i in subs:
            print(i)
            sub_names.append(i)
        return sub_names

        for s in subs:
            name = '/r/{}'.format(s)
            choice = (name, name)
            sub_names.append(choice)  # choices must be tuples
        return sub_names


class SearchReddit(Resource):
    @marshal_with(item_fields)
    def get(self, query):
        subreddits = query.split('+')
        reddit_posts = reddit.fetch_submissions(subreddits)  # praw submission objects
        items = generate_items(reddit_posts)  # custom objects
        # return filter(lambda i: i is not None, items)
        return [i for i in items if i]


class Search(Resource):
    @marshal_with(item_fields)
    def get(self):
        args = parser.parse_args()
        reddit_query = args.get('reddit_query') or ''
        sc_query = args.get('sc_query') or ''

        subreddits = reddit_query.split('+')
        reddit_posts = reddit.fetch_submissions(subreddits)

        sc_artists = sc_query.split('+')
        sc_tracks = sc.fetch_tracks(sc_artists)

        items = generate_items(reddit_posts, sc_tracks) # adds to db
        # return items
        return [i for i in items if i]


class ProtectedResource(Resource):
    method_decorators = [jwt_required]


class UserResource(ProtectedResource):
    @marshal_with(user_fields)
    def get(self):
        # jwt_extended requires json serializable identity
        # so need to perform query from username
        username = get_jwt_identity()
        user = User.query.filter(User.username == username).scalar()
        return user

class Favorite(ProtectedResource):
    """Add or remove item from favorites favorites"""

    def parse_item(self, item_obj):
        track_id, source = item_obj['track_id'], item_obj['source']
        return get_or_create(db.session, Item, track_id=track_id, source=source)

    @marshal_with(user_fields)
    def put(self):
        """Remove item from favorites and return the updated User object"""
        print('Deleting item')
        user = get_jwt_identity()
        item_obj = request.get_json()['item']
        item = self.parse_item(item_obj)
        if item in user.favorites:
            user.favorites.remove(item)
            db.session.add(item)
            db.session.add(user)
            db.session.commit()
        return get_jwt_identity()


    @marshal_with(user_fields)
    def post(self):
        """Save item to favorites and return the updated User object"""
        item_obj = request.get_json()['item']
        item = self.parse_item(item_obj)
        item.raw_title = item_obj['raw_title']  # title seperate bc title may change with post
        item.domain = item_obj['domain']
        item.url = item_obj['url']
        user = get_jwt_identity()

        if item not in user.favorites:
            user.favorites.append(item)
            db.session.add(item)
            db.session.add(user)
            db.session.commit()

        return get_jwt_identity()

class Auth(Resource):
    """docstring for Auth"""

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = User.query.filter(User.username == username).scalar()
        if user and bcrypt.check_password_hash(user.password, password):
            return {'access_token': create_access_token(identity=username)}


api.add_resource(Auth, '/auth')


api.add_resource(UserResource, '/users')
api.add_resource(Favorite, '/users/favorites')

api.add_resource(HelloWorld, '/')
api.add_resource(RedditSources, '/reddit/sources')
api.add_resource(SearchReddit, '/reddit/<string:query>')
api.add_resource(Search, '/search')  # queried using /search
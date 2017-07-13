from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required, current_identity

from amnisiac.sources import reddit, sc
from amnisiac.sources.utilities import generate_items

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

        items = generate_items(reddit_posts, sc_tracks)
        # return items
        return [i for i in items if i]


class ProtectedResource(Resource):
    method_decorators = [jwt_required()]


class User(ProtectedResource):
    @marshal_with(user_fields)
    def get(self):
        return current_identity


api.add_resource(User, '/users')

api.add_resource(HelloWorld, '/')
api.add_resource(RedditSources, '/reddit/sources')
api.add_resource(SearchReddit, '/reddit/<string:query>')
api.add_resource(Search, '/search')  # queried using /search

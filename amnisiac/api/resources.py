from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from amnisiac.sources import reddit
from amnisiac.sources.utilities import generate_items

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('')



item_fields = {
    # 'id': fields.Integer,
    'track_id': fields.String,
    'raw_title': fields.String,
    # 'title': fields.String,
    # 'artist': fields.String,
    'url': fields.String,
    'domain': fields.String,
    # 'date_published': fields.DateTime,
    'date_saved': fields.DateTime,
    'source': fields.String,
    'subreddit': fields.String
}   


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class SearchReddit(Resource):
    @marshal_with(item_fields)
    def get(self, query):
        subreddits = query.split('+')
        reddit_posts = reddit.fetch_submissions(subreddits) # praw submission objects
        items = generate_items(reddit_posts)  # custom objects
        # return filter(lambda i: i is not None, items)
        return [i for i in items if i]


api.add_resource(HelloWorld, '/')
api.add_resource(SearchReddit, '/reddit/<string:query>')

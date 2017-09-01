from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from amnisiac.reddit import utils


reddit_blueprint = Blueprint('reddit', __name__, url_prefix='/reddit')
api = Api(reddit_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('reddit_query')
# parser.add_argument('sc_query')


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


class RedditSources(Resource):
    """Returns list of all registered music-wiki subreddits"""

    def get(self):
        sub_names = []
        subs = utils.wiki_subs('music', 'musicsubreddits')
        for i in subs:
            sub_names.append(i)
        return sub_names


# class SearchReddit(Resource):
#     @marshal_with(item_fields)
#     def get(self, query):
#         """Returns latest items from queried subreddits"""
#         subreddits = query.split('+')
#         reddit_posts = utils.fetch_submissions(subreddits)  # praw submission objects
#         items = utils.generate_items(reddit_posts)  # custom objects
#         # return filter(lambda i: i is not None, items)
#         return [i for i in items if i]


class Search(Resource):
    """Returns latest items from queried subreddits"""
    @marshal_with(item_fields)
    def get(self):
        args = parser.parse_args()
        reddit_query = args.get('reddit_query') or ''

        subreddits = reddit_query.split('+')
        reddit_posts = utils.fetch_submissions(subreddits)

        items = utils.generate_items(reddit_posts)  # adds to db
        # return items
        return [i for i in items if i]



api.add_resource(RedditSources, '/sources')
api.add_resource(Search, '/search')





# TODO: move to sc blueprint when implemented
# class Search(Resource):
#     @marshal_with(item_fields)
#     def get(self):
#         args = parser.parse_args()
#         reddit_query = args.get('reddit_query') or ''
#         sc_query = args.get('sc_query') or ''

#         subreddits = reddit_query.split('+')
#         reddit_posts = reddit.fetch_submissions(subreddits)

#         sc_artists = sc_query.split('+')
#         sc_tracks = sc.fetch_tracks(sc_artists)

#         items = generate_items(reddit_posts, sc_tracks)  # adds to db
#         # return items
#         return [i for i in items if i]

# api.add_resource(Search, '/search')  # queried using /search

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from amnisiac.reddit import utils as reddit
from amnisiac.soundcloud import utils as sc
from amnisiac.models import feed_fields, item_fields


reddit_blueprint = Blueprint('reddit', __name__, url_prefix='/reddit')
api = Api(reddit_blueprint)

parser = reqparse.RequestParser()
parser.add_argument('reddit_query')
parser.add_argument('sc_query')


class RedditSources(Resource):
    """Returns list of all registered music-wiki subreddits"""

    def get(self):
        sub_names = []
        subs = reddit.wiki_subs('music', 'musicsubreddits')
        for i in subs:
            sub_names.append(i)
        return sub_names


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

        items = reddit.generate_items(reddit_posts, sc_tracks)  # adds to db   # need to move generate to models.py
        # return items
        return [i for i in items if i]

# class Search(Resource):
#     """Returns latest items from queried subreddits"""
#     @marshal_with(item_fields)
#     def get(self):
#         args = parser.parse_args()
#         reddit_query = args.get('reddit_query') or ''

#         subreddits = reddit_query.split('+')
#         reddit_posts = utils.fetch_submissions(subreddits)

#         items = utils.generate_items(reddit_posts)  # adds to db
#         return [i for i in items if i]


api.add_resource(RedditSources, '/sources')
api.add_resource(Search, '/search')

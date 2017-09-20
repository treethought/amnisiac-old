# amnisiac/platforms/resources.py
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with


from amnisiac.models import item_fields

from amnisiac.platforms import reddit, sc, utils


platforms_blueprint = Blueprint('platforms', __name__, url_prefix='/platforms')
api = Api(platforms_blueprint)

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

        items = utils.generate_items(reddit_posts, sc_tracks)  # adds to db
        return [i for i in items if i]


@platforms_blueprint.route('/sc_autocomplete', methods=['GET'])
def autocomplete():
    results = []
    term = request.args.get('q')
    for user in sc.search_user(term):
        if term.lower() in user.username.lower():
            print(user.username.lower())
            results.append(user.username)

    return jsonify(results=results)


api.add_resource(RedditSources, '/reddit/sources')
api.add_resource(Search, '/search')

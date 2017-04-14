# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, session

from project.server.reddit.forms import RedditSearchForm
from project.server.sc.forms import ScSearchForm
from project.server.reddit.api import build_sources, fetch_submissions

from typing import List, Dict

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    reddit_form = RedditSearchForm()
    reddit_form.follow_sources.choices = build_sources()
    reddit_form.process()
    sc_form = ScSearchForm()
    return render_template('main/home.html', reddit_form=reddit_form, sc_form=sc_form)


# def gather_items(reddit_query: List[str], sc_query=List[str]) -> Dict[] :
#     items = {}
#     reddit_posts = fetch_submissions(session['reddit_query'])



@main_blueprint.route('/results', methods=['POST'])
def results():
    reddit_form = RedditSearchForm(request.form)
    submissions = []

    sc_form = ScSearchForm(request.form)
    call_sc = False

    # TODO!! render feed for reddit/sc the same way
    # riht now: 
        # reddit: loads ons server, sends list of objectsto template
        # sc: stores query in session, page loads send ajax to sc view to retrieve results (bc slower)

    if reddit_form.reddit_search.data and reddit_form.validate_on_submit():
        subreddits = reddit_form.reddit_search.data.split(',')
        submissions = fetch_submissions(subreddits)

    if sc_form.sc_search.data and sc_form.validate_on_submit():
        session['sc_artists'] = sc_form.sc_search.data
        call_sc = True

        
    return render_template('main/results.html', submissions=submissions, call_sc=call_sc)


@main_blueprint.route('/sources', methods=['GET', 'POST'])
def sources():
    subs = build_sources()
    form = SourcesForm(request.form)
    form.follow_sources.choices = subs
    form.process()
    return render_template('main/sources.html', form=form)

# @main_blueprint.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     print(request)
#     result = []
#     term = request.args.get('q')
#     app.logger.debug(term)

#     for sub in wiki_subs('music', 'musicsubreddits'):
#         if term in sub[:len(term)]:
#             print('found {} in {}'.format(term, sub))
#             result.append(sub)

#     return jsonify(matching_results=result)


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

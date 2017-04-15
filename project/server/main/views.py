# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, session

from project.server.reddit.forms import RedditSearchForm
from project.server.sc.forms import ScSearchForm
from project.server.main.forms import HomeSearchForm
from project.server.reddit.api import build_sources, fetch_submissions
from project.server.sc.api import fetch_tracks

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
    search_form = HomeSearchForm()
    search_form.follow_sources.choices = build_sources()
    search_form.process()
    return render_template('main/home.html', form=search_form)


@main_blueprint.route('/results', methods=['POST'])
def results():
    reddit_form = RedditSearchForm(request.form)
    sc_form = ScSearchForm(request.form)

    items = []

    if reddit_form.reddit_search.data and reddit_form.validate_on_submit():
        subreddits = reddit_form.reddit_search.data.split(',')
        items.extend(fetch_submissions(subreddits))

    if sc_form.sc_search.data and sc_form.validate_on_submit():
        sc_artists = sc_form.sc_search.data.split(',')
        items.extend(fetch_tracks(sc_artists))

    return render_template('main/results.html', items=items)


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

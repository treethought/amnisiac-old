# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request

from project.server.reddit.forms import RedditSearchForm
from project.server.sc.forms import ScSearchForm
from project.server.reddit.api import build_sources, fetch_submissions

from typing import List

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



@main_blueprint.route('/results', methods=['POST'])
def results():
    reddit_form = RedditSearchForm(request.form)
    submissions = []

    sc_form = ScSearchForm(request.form)

    if reddit_form.search_bar.data and reddit_form.validate_on_submit():
        print('submitted bitch')
        subreddits = reddit_form.search_bar.data.split(',')
        submissions = fetch_submissions(subreddits)

    if sc_form.search_bar.data and sc_form.validate_on_submit():
        pass

        
    return render_template('main/results.html', submissions=submissions)


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

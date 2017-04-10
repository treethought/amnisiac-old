# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, make_response, url_for, jsonify
from flask_login import login_required, current_user

from project.server.main.forms import SearchForm, SourcesForm
from project.server.scrapers.reddit_links import hot_posts, wiki_subs, split_by_domain, build_sources
from project.server.models import User, Feed, get_or_create
from project.server import db, app
from flask_sqlalchemy import BaseQuery, Pagination


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = SourcesForm(request.form)
    form.follow_sources.choices = build_sources()
    form.process()
    return render_template('main/home.html', form=form, sources=sources)


@main_blueprint.route('/autocomplete', methods=['GET'])
def autocomplete():
    print(request)
    result = []
    term = request.args.get('q')
    app.logger.debug(term)

    for sub in wiki_subs('music', 'musicsubreddits'):
        if term in sub[:len(term)]:
            print('found {} in {}'.format(term, sub))
            result.append(sub)

    return jsonify(matching_results=result)


@main_blueprint.route('/results', methods=['POST'])
def results():
    form = SourcesForm(request.form)
    sub_query = ''
    if form.validate_on_submit():
        subreddits = form.search_bar.data.split(',')
        for sub in subreddits:
            sub_query += sub.strip(',').strip('/r/') + '+'

        submissions = hot_posts(sub_query)
        by_domain = split_by_domain(submissions)
        return render_template('main/results.html', subreddit=subreddits, by_domain=by_domain)


@main_blueprint.route('/sources', methods=['GET', 'POST'])
def sources():
    subs = build_sources()
    form = SourcesForm(request.form)
    form.follow_sources.choices = subs
    form.process()
    return render_template('main/sources.html', form=form)


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

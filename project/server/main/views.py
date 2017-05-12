# project/server/main/views.py


#################
#### imports ####
#################
import itertools

from flask import render_template, Blueprint, request, session, redirect, url_for
from flask_login import current_user


from project.server.main.forms import HomeSearchForm
from project.server.reddit.api import build_sources, fetch_submissions
from project.server.sc.api import fetch_tracks

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/', methods=['GET'])
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('main.home'))


@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    search_form = HomeSearchForm()
    search_form.follow_sources.choices = build_sources()
    search_form.process()
    return render_template('main/home.html', form=search_form)


@main_blueprint.route('/results', methods=['POST'])
def results():
    form = HomeSearchForm(request.form)
    items = []

    if form.validate_on_submit():
        subreddits = form.reddit_search.data.split(',')
        reddit_posts = fetch_submissions(subreddits)

        sc_artists = form.sc_search.data.split(',')
        sc_tracks = fetch_tracks(sc_artists)

        for i in list(itertools.zip_longest(reddit_posts, sc_tracks)):
            items.extend(i)

    return render_template('main/results.html', items=items)


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

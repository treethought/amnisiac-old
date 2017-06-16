# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from flask_login import current_user


from project.server.main.forms import HomeSearchForm
from project.server.sources import reddit, sc
from project.server.sources.utilities import generate_items

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
    search_form.follow_sources.choices = reddit.build_sources()
    search_form.process()
    return render_template('main/home.html', form=search_form)


# TODO: remove from sc.views and use select2
@main_blueprint.route('/sc_autocomplete', methods=['GET'])
def autocomplete():
    results = []
    term = request.args.get('q')
    for user in sc.search_user(term):
        if term.lower() in user.username.lower():
            results.append(user.username)

    return jsonify(results=results)


@main_blueprint.route('/results', methods=['POST'])
def results():
    form = HomeSearchForm(request.form)
    items = []

    if form.validate_on_submit():
        subreddits = form.reddit_search.data.split(',')
        reddit_posts = reddit.fetch_submissions(subreddits)
        sc_artists = form.sc_search.data.split(',')
        sc_tracks = sc.fetch_tracks(sc_artists)

        items = generate_items(reddit_posts, sc_tracks)

    return render_template('main/results.html', items=items)


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

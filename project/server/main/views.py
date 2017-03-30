# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, make_response, url_for, jsonify
from flask_login import login_required, current_user

from project.server.main.forms import PostForm, SourcesForm
from project.server.scrapers.reddit_links import hot_posts, wiki_subs
from project.server.models import User, Feed, get_or_create
from project.server import db


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)

# @app.context_processor
# def utility_processor():
#     def format_price(amount, currency=u'€'):
#         return u'{0:.2f}{1}'.format(amount, currency)
#     return dict(format_price=format_price)

def build_sources():
    subs = wiki_subs('music', 'musicsubreddits')
    sub_names = []
    for s in subs:
        name = '/r/{}'.format(s)
        choice = (name, name)
        sub_names.append(choice)  # choices must be tuples
    return sub_names


################
#### routes ####
################

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = PostForm(request.form)
    return render_template('main/home.html', form=form)

@main_blueprint.route('/results', methods=['POST'])
def results():
    form = PostForm(request.form)
    if form.validate_on_submit():
        subreddit = form.subreddit.data
        submissions = hot_posts(subreddit)
        # submissions = hot_posts('mathrock')
        return render_template('main/results.html', subreddit=subreddit, submissions=submissions)

@main_blueprint.route('/sources', methods=['GET', 'POST'])
def sources():
    subs = build_sources()
    form = SourcesForm(request.form)
    form.follow_sources.choices = subs
    form.process()
    return render_template('main/sources.html', form=form)

@main_blueprint.route('/add_sources', methods=['POST'])
@login_required
def add_sources():
    form = SourcesForm(request.form)
    selected = form.follow_sources.data
    user = current_user
    for source in selected:
        name, url = source, 'http://reddit.com'+source
        feed = get_or_create(db.session, Feed, name=name, url=url)
        if feed not in user.feeds:
            user.feeds.append(feed)
        
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.dashboard'))



@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

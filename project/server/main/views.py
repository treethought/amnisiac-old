# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, make_response, url_for, jsonify
from flask_login import login_required, current_user

from project.server.main.forms import PostForm, SourcesForm
from project.server.scrapers.reddit_links import hot_posts, wiki_subs, split_by_domain
from project.server.models import User, Feed, get_or_create
from project.server import db, app


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

# @main_blueprint.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     print(request)
#     search = request.args.get('term')
#     app.logger.debug(search)
#     return jsonify(['test', '1', '2'])



@main_blueprint.route('/results', methods=['POST'])
def results():
    form = PostForm(request.form)
    if form.validate_on_submit():
        subreddits = form.subreddit.data.replace(' ', '+').replace(',', '')
        submissions = hot_posts(subreddits)
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

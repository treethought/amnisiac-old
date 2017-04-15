# project/server/user/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db, app
from project.server.models import User, Feed, get_or_create
from project.server.user.forms import LoginForm, RegisterForm
from project.server.reddit.api import build_sources, fetch_submissions
from project.server.reddit.forms import RedditSearchForm
from project.server.main.forms import HomeSearchForm

from project.server.sc.api import get_user, fetch_tracks

from typing import List

################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/dashboard')
@login_required
def dashboard():
    subs = []
    sc_artists = []

    for feed in current_user.feeds:
        if feed.domain == 'reddit':
            subs.append(feed.name.strip().strip('/r/'))
        elif feed.domain == 'sc':
            sc_artists.append(feed.name)

    reddit_posts = fetch_submissions(subs)
    sc_tracks = fetch_tracks(sc_artists)

    items = sum(map(list, zip(reddit_posts, sc_tracks)), [])

    return render_template('user/dashboard.html', user=current_user, items=items)


@user_blueprint.route('/manage_sources', methods=['GET', 'POST'])
@login_required
def manage_sources():
    new_sources = build_sources()
    new = HomeSearchForm()
    new.follow_sources.choices = new_sources
    new.process()

    current = RedditSearchForm(request.form)
    current_choice_tups = [(f.name, f.name) for f in current_user.feeds]
    current.follow_sources.choices = current_choice_tups
    current.process()

    return render_template('user/manage_sources.html', new=new, current=current)


@user_blueprint.route('/add_sources', methods=['POST'])
@login_required
def add_sources():
    items = {}
    user = current_user
    form = HomeSearchForm(request.form)

    if form.validate_on_submit():
        reddits = form.reddit_search.data.strip().split(',')
        sc_artists = form.sc_search.data.strip().split(',')

    for source in filter(None, reddits):
        app.logger.debug('adding {} from reddit'.format(source))
        name, url = source, 'http://reddit.com' + source
        feed = get_or_create(db.session, Feed, name=name, url=url, domain='reddit')
        if feed not in current_user.feeds:
            user.feeds.append(feed)

    for source in filter(None, sc_artists):
        app.logger.debug('adding {} from sc'.format(source))
        artist = get_user(source)
        name, url = source, artist.permalink_url
        feed = get_or_create(db.session, Feed, name=name, url=url, domain='sc')
        if feed not in user.feeds:
            user.feeds.append(feed)

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.manage_sources'))


@user_blueprint.route('/remove_sources', methods=['POST'])
@login_required
def remove_sources():
    form = RedditSearchForm(request.form)
    selected = form.follow_sources.data
    user = current_user
    current_feeds = user.feeds
    for s in selected:
        feed = get_or_create(db.session, Feed, name=s)
        try:
            current_feeds.remove(feed)
        except ValueError:
            raise  # or scream: thing not in some_list!
        except AttributeError:
            raise  # call security, some_list not quacking like a list!

    user.feeds = current_feeds
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.manage_sources'))


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.dashboard"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')

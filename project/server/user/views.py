# project/server/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User, Feed, get_or_create
from project.server.user.forms import LoginForm, RegisterForm
from project.server.scrapers.reddit_links import hot_posts, split_by_domain
from project.server.main.forms import SourcesForm

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
    feed_data = {}
    sub_query = ''
    by_domain = {}
    for feed in current_user.feeds:
        sub_query += feed.name.strip('/r/') + '+'

    if sub_query:
        submissions = hot_posts(sub_query)
        by_domain = split_by_domain(submissions)
        

    return render_template('user/dashboard.html', user=current_user, by_domain=by_domain)



@user_blueprint.route('/add_sources', methods=['POST'])
@login_required
def add_sources():
    form = SourcesForm(request.form)
    selected = form.search_bar.data.split(',')
    user = current_user
    for source in selected:
        name, url = source, 'http://reddit.com'+source
        feed = get_or_create(db.session, Feed, name=name, url=url)
        if feed not in user.feeds:
            user.feeds.append(feed)
        
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.dashboard'))


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

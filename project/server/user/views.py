# project/server/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm
from project.server.scrapers.reddit_links import hot_posts
from project.server.scrapers.video_ids import vimeo_id, youtube_id
################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)





################
#### routes ####
################

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

def split_by_domain(submissions):
    domains = {'youtube': [], 'vimeo': []}
    yt_posts = [p for p in submissions if 'you' in p.domain]
    for p in [p for p in yt_posts if p.video_id]:
        if len(p.video_id) == 11:
            print(p.video_id)
            print('***********')
            domains['youtube'].append(p)


    # domains['youtube'] = [p for p in submissions if 'you' in p.domain and p.video_id and len(p.video_id) == 11]
    domains['vimeo'] = [p for p in submissions if 'vim' in p.domain]
    print(domains)
    return domains

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


    print('RENDERING FOR {} submissions'.format(len(submissions)))
    return render_template('user/dashboard.html', user=current_user, by_domain=by_domain)

    # else:
    #     return render_template('user/dashboard.html', user=current_user)


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

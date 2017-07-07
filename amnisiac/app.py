# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template


from amnisiac import commands, main, user, api
from amnisiac.assets import assets
from amnisiac.extensions import admin, bcrypt, bootstrap, db, debug_toolbar, login_manager, migrate # , cach, csrf_protect
from amnisiac.settings import ProdConfig
from amnisiac.models import User, Feed, Item
from amnisiac.utils import AdminModelView


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0], static_url_path='/static')
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_admin(app)  # after sqlalchemy init (db
    return app

def register_admin(app):
    admin.init_app(app)
    admin.add_view(AdminModelView(Feed, db.session))
    admin.add_view(AdminModelView(Item, db.session))
    admin.add_view(AdminModelView(User, db.session, endpoint='user_admin'))

def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    # cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main.views.main_blueprint)
    app.register_blueprint(user.views.user_blueprint)
    app.register_blueprint(api.resources.api_blueprint)
    return None
    


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

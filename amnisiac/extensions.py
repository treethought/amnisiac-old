# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from flask_restful import Api
# from flask_wtf.csrf import CSRFProtect

admin = Admin()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
# csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
cors = CORS()
# jwt = JWT()
jwt = JWTManager()
# api = Api()

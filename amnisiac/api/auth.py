from flask_jwt import jwt_required, current_identity

from amnisiac.extensions import bcrypt, jwt
from amnisiac.models import User



@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter(User.username == username).scalar()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

@jwt.identity_handler
def identify(payload):
    return User.query.filter(User.id == int(payload['identity'])).first()


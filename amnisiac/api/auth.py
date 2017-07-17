# from flask import request
# from flask_jwt_extended import create_access_token

# from amnisiac.extensions import bcrypt, jwt
# from amnisiac.models import User
# from amnisiac.api.resources import api




# @jwt.authentication_handler
# def authenticate(username, password):
#     user = User.query.filter(User.username == username).scalar()
#     if user and bcrypt.check_password_hash(user.password, password):
#         print(user)
#         return user

# @jwt.identity_handler
# def identify(payload):
#     return User.query.filter(User.id == int(payload['identity'])).first()


# class Auth(Resource):
#     """docstring for Auth"""

#     def post(self):
#         username = request.json.get('username', None)
#         password = request.json.get('password', None)
#         user = User.query.filter(User.username == username).scalar()
#         if user and bcrypt.check_password_hash(user.password, password):
#             return {'access_token': create_access_token(identity=user)}


# api.add_resource(Auth, '/auth')

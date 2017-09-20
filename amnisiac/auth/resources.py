import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, \
    create_access_token, create_refresh_token
from amnisiac.extensions import db, bcrypt
from amnisiac.models import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """Creates and returns access and refresh tokens"""
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter(User.username == username).scalar()

    if user and bcrypt.check_password_hash(user.password, password):
        access = create_access_token(identity=username)
        refresh = create_refresh_token(identity=username)

        resp = {'access_token': access, 'refresh_token': refresh}
        return jsonify(resp), 200

    else:
        return jsonify({'msg': "Bad username or password"}), 401


@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    instance = db.session.query(User).filter_by(username=username).first()

    if instance is None:
        instance = User(username=username, password=password)
        db.session.add(instance)
        db.session.commit()

    resp = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }
    return jsonify(resp), 200


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # this is username used for jwt tokens, not the User object
    current_identity = get_jwt_identity()
    resp = {'access_token': create_access_token(identity=current_identity)}
    return jsonify(resp), 200

@auth_blueprint.route('/sc_client', methods=['GET'])
def sc_client():
    client_id = os.getenv('SOUNDCLOUD_CLIENT_ID')
    return jsonify(client_id), 200

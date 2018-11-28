import hashlib

from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

from currenciesapp import db
from currenciesapp.token_auth import check_auth, generate_auth_token, remove_user
from currenciesapp.data_models import Users

users = Blueprint('users', __name__)


@users.route("/login", methods=['POST'])
@cross_origin()
def login():
    json = request.get_json()
    if not json:
        abort(400)
    keys = ['username', 'password']
    if any(key not in list(json.keys()) for key in keys):
        abort(422)
    auth = check_auth(json['username'], json['password'])
    if not auth:
        abort(401)
    token = generate_auth_token(json['username'])
    return jsonify(token=token.decode('utf-8'))


@users.route("/logout", methods=['GET', 'POST'])
@cross_origin()
def logout():
    token = request.headers.get('Token')
    remove_user(token)
    return jsonify(errorCode='0')


@users.route("/check_username", methods=['POST'])
@cross_origin()
def check_username():
    json = request.get_json()
    if not json:
        abort(400)
    if 'username' not in json:
        abort(422)
    user = Users.query.filter_by(username=json['username']).first()
    if user:
        return jsonify(errorCode='0001', errorDesc=f"Login {json['username']} jest już zajęty")
    return jsonify(errorCode='0')


@users.route("/user/register", methods=['POST'])
@cross_origin()
def register():
    json = request.get_json()
    if not json:
        abort(400)
    keys = ['username', 'password', 'email', 'firstName', 'lastName']
    if any(key not in list(json.keys()) for key in keys):
        abort(422)
    user_check = Users.query.filter_by(username=json['username']).first()
    if user_check:
        return jsonify(errorCode='0001', errorDesc=f"Login {json['username']} jest już zajęty")
    if '@' not in json['email'] or '.' not in json['email']:
        return jsonify(errorCode='0002', errorDesc=f"Adres email {json['email']} jest niepoprawny")
    if len(json['password']) < 8:
        return jsonify(errorCode='0003', errorDesc=f"Hasło jest za krótkie. Hasło powinno mieć co najmniej 8 znaków.")
    password_hash = hashlib.sha512(json['password'].encode('utf-8')).hexdigest()
    user = Users(username=json['username'], email=json['email'], password=password_hash,
                 first_name=json['firstName'], last_name=json['lastName'])
    db.session.add(user)
    db.session.commit()
    return jsonify(errorCode='0', errorDesc='OK')

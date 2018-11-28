import hashlib
from functools import wraps

from flask import request, abort
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from currenciesapp import db
from currenciesapp.config import Config, EXPIRATION_TIME
from currenciesapp.data_models import Users


def check_auth(username: str, password: str):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return False
    user_password_hash = user.password
    pass_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    if pass_hash.lower() == user_password_hash.lower():
        return True
    return False


def generate_auth_token(username, expiration=EXPIRATION_TIME):
    s = Serializer(Config.SECRET_KEY, expires_in=expiration)
    token = s.dumps({'username': username})
    user = Users.query.filter_by(username=username).first()
    user.token = token.decode('utf-8')
    db.session.commit()
    return token


def verify_auth_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    user = Users.query.filter_by(token=token).first()
    if not user:
        return False
    if user.username == data['username']:
        return True
    return False


def remove_user(token):
    user = Users.query.filter_by(token=token).first()
    if user:
        user.token = ''
        db.session.commit()


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Token')
        if not token or not verify_auth_token(token):
            abort(403)
        return f(*args, **kwargs)

    return decorated

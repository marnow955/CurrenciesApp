from flask import Blueprint, jsonify
from flask_cors import cross_origin


users = Blueprint('users', __name__)


@users.route("/login", methods=['POST'])
@cross_origin()
def login():
    return jsonify(token='$sdasdae!#23ewrewfsdfsdr3r23413212edwadsDVSDFSf')


@users.route("/logout", methods=['GET', 'POST'])
@cross_origin()
def logout():
    return jsonify(errorCode='0')


@users.route("/check_username", methods=['POST'])
@cross_origin()
def check_username():
    return jsonify(errorCode='0001', errorDesc='Login xxx jest już zajęty')


@users.route("/user/register", methods=['POST'])
@cross_origin()
def register():
    return jsonify(errorCode='0', errorDesc='OK')

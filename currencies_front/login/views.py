from flask import Flask, Blueprint, request, redirect, render_template, session, flash
from flask_cors import cross_origin
import requests

login = Blueprint('login', __name__)

API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'login'


@login.route("/login", methods=['POST'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    data = {'username': username, 'passwors': password}
    token = requests.post(LOGIN_URL, json=data)
    if not token:
        return redirect('/home')
    else:
        return redirect('/predictions')

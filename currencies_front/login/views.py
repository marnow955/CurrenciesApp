from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

login = Blueprint('login', __name__)

API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'login'


@login.route("/login", methods=['POST'])
@cross_origin()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form['username']
        password = form['password']
        data = {'username': username, 'passwors': password}
        token = requests.post(LOGIN_URL, json=data)
    return render_template('login.html', title='Logowanie')

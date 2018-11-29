from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

from currencies_front.login.forms import LoginForm

login_blueprint = Blueprint('login', __name__)

API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'login'


@login_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form['username'].data
        password = form['password'].data
        data = {'username': username, 'password': password}
        response = requests.post(LOGIN_URL, json=data)
        json = response.json()
        print(json['token'])
    return render_template('login.html', title='Logowanie', form=form)

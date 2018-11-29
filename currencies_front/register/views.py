from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

from currencies_front.register.forms import RegistrationForm

login_blueprint = Blueprint('login', __name__)

API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'user/register'


@login_blueprint.route("/register", methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form['username'].data
        password = form['password'].data
        first_name = form['first_name'].data
        last_name = form['last_name'].data
        email = form['email'].data
        data = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name,
                'email': email}
        response = requests.post(LOGIN_URL, json=data)
        json = response.json()
        print(json['token'])
    return render_template('register.html', title='Rejestracja', form=form)

from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

from currencies_front.register.forms import RegistrationForm

register_blueprint = Blueprint('register', __name__)

API_URL = 'http://localhost:5000/'
REGISTER_URL = API_URL + 'user/register'


@register_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form['username'].data
        password = form['password'].data
        first_name = form['first_name'].data
        last_name = form['last_name'].data
        email = form['email'].data
        data = {'username': username, 'password': password, 'firstName': first_name, 'lastName': last_name,
                'email': email}
        response = requests.post(REGISTER_URL, json=data)
        json = response.json()
        print(json)
    return render_template('register.html', title='Rejestracja', form=form)

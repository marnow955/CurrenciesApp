from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

login = Blueprint('login', __name__,url_prefix='/login')
API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'login'


@login.route("", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    data = {'username': username, 'passwors': password}
    token = requests.post(LOGIN_URL, json=data)
    if not token:
        redirect('/home')
    else:
        redirect('/predictions')
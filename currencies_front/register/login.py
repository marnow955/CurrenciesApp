from flask import Flask, Blueprint, request, redirect, render_template, session, flash
import requests

login = Blueprint('predictions', __name__)
API_URL = 'http://localhost:5000/'
LOGIN_URL = API_URL + 'login'

@login.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    data = {'username': username, 'passwors': password}
    token = requests.post(LOGIN_URL, json=data)
    if not token:
        redirect('/home')

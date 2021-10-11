from flask import Flask, render_template, request, redirect

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class GetUsername(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'

# api = requests.get("https://data.covidapi.com/countries").json()

@app.route("/", methods = ["GET", "POST"])
def index():
    form = GetUsername(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        return redirect((f'/user?username={username}'))
    return render_template('index.html', form=form)

@app.route("/user", methods = ["GET", "POST"])
def user():
    if "username" in request.args:
        username = request.args["username"]
        return username
    else:
        redirect("/")
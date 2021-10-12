from flask import Flask, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'


class GetUsername(FlaskForm):
    username = StringField('username', validators=[DataRequired()])


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

        user = requests.get(f"https://api.github.com/users/{username}").json()
        repos = requests.get(f"https://api.github.com/users/{username}/repos").json()
        gists = requests.get(f"https://api.github.com/users/{username}/gists").json()
        followers = requests.get(f"https://api.github.com/users/{username}/followers").json()
        following = requests.get(f"https://api.github.com/users/{username}/following").json()

        return render_template(
            "user.html",
            user = user,
            len_repos = len(repos), repos = repos,
            len_gists = len(gists), gists = gists,
            len_followers = len(followers), followers = followers,
            len_following = len(following), following = following
        )
    else:
        redirect("/")

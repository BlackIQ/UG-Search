from flask import Flask, redirect, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'


class GetUsername(FlaskForm):
    username = StringField('username', validators=[DataRequired()])


@app.route("/", methods=["GET", "POST"])
def index():
    form = GetUsername(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        return redirect(f'/user/{username}')
    return render_template('index.html', form=form)


@app.route("/user", methods=["GET", "POST"])
def user():
    flash('You should enter a username')
    return redirect("/")


@app.route("/user/<string:username>", methods=["GET", "POST"])
def user_search(username):
    get_user_request = requests.get(f"https://api.github.com/users/{username}")

    if get_user_request.ok:

        user = get_user_request.json()
        repos = requests.get(f"https://api.github.com/users/{username}/repos").json()
        gists = requests.get(f"https://api.github.com/users/{username}/gists").json()
        followers = requests.get(f"https://api.github.com/users/{username}/followers").json()
        following = requests.get(f"https://api.github.com/users/{username}/following").json()

        if user["type"] == "User":
            return render_template(
                "user.html",
                user=user,
                len_repos=len(repos), repos=repos,
                len_gists=len(gists), gists=gists,
                len_followers=len(followers), followers=followers,
                len_following=len(following), following=following
            )
        else:
            flash("The username is for an organization")
            return redirect("/")

    elif get_user_request.status_code == 404:
        flash("User not found")
        return redirect("/")

    elif get_user_request.status_code == 403:
        flash("Api not responding, please try again later")
        return redirect("/")

    else:
        flash("Unexpected problem")
        return redirect("/")

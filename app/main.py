from flask import Flask, render_template
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234'

api = requests.get("https://data.covidapi.com/countries").json()

@app.route("/")
def index():
    # return "Hi"
    return render_template("index.html")
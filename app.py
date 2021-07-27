# Library imports
import json
import os
import sqlite3

from flask import Flask, redirect, request, url_for
from flask_login import (
        LoginManager,
        current_user,
        login_required,
        login_user,
        logout_user
        )

from oauthlib.oauth2 import WebApplicationClient
from werkzeug.utils import secure_filename
import requests

# Local imports
import db # for init_db_command, init_app
from user import User
import process

from dotenv import load_dotenv
load_dotenv()

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL", None)

# Application setup
app = Flask(__name__)
app.config['DATABASE'] = "sqlite-db"
# app.config['UPLOAD_FOLDER'] = "/home/ashwin/Documents/Repos/mine/KakchoAssignment/dataset-categorizer/data/"
app.secret_key = os.environ.get("SECRET_KEY")

# Uesr authentication setup
login_manager = LoginManager()
login_manager.init_app(app)

# DB setup
try:
    db.init_db_command()
except: sqlite3.OperationalError

# Goolge OAuth2 setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Login helper
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Defining endpoints
@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
                "<p>Hello, {}! You're logged in! Email: {}</p>"
                '<a class="button" href="/logout">Logout</a>'
                """ <form action = "https://127.0.0.1:5000/upload" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   """
      .format(
          current_user.name, current_user.email,
          )
      )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope = ["openid", "email", "profile"],
            )
    print(request.base_url + "/callback")
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Retrieving the authorization code from Google's request to this endpoint
    authCode = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Create the token request with the received authorization code and token endpoint
    token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=authCode
            )
    token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
            )
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Getting the user's profile from Google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Creating an entry in the database with the received info
    if not User.get(unique_id):
        User.create(id_=unique_id, name=users_name, email=users_email)

    # Begin user session
    user = User(id_=unique_id, name=users_name, email=users_email)
    login_user(user)

    return redirect(url_for("index"))

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(secure_filename(f.filename))
        return ('<p><a href="/paymentFilter/{}">Filter by payment</a></p>'
                '<p><a href="/ratingFilter/{}">Filter by ratings</a></p>'
                '<p><a href="/roundOffRatings/{}">Round off ratings</a></p>'.format(
                    filename, filename, filename
                    )
                )

@app.route("/paymentFilter/<filename>")
def paymentFilter(filename):
    return process.paymentFilter(filename)

@app.route("/ratingFilter/<filename>")
def ratingFilter(filename):
    return process.contentRatingFilter(filename)

@app.route("/roundOffRatings/<filename>")
def roundOffRatings(filename):
    return process.roundOffRatings(filename)

if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)

# Library imports

from flask_restful import Api, Resource
import json
import os

from flask import Flask, redirect, request, url_for
from flask_login import (
        LoginManager,
        current_user,
        login_required,
        login_user,
        logout_user
        )

from oauthlib.oauth2 import WebApplicationClient
import requests

# Local imports

app = Flask(__name__)
api = Api(app)
app.config['DATABASE'] = "sqlite-db"

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template
from flask_session import Session
from helpers import login_required
from database import db
from auth import auth_bp
from card_collections import collections_bp
from cards import cards_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(collections_bp)
app.register_blueprint(cards_bp)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")
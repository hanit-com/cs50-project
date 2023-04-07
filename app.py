import os

from cs50 import SQL
from flask import Flask, redirect, render_template, jsonify, request, session
from helpers import render_error_template, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# MARK: - Index

@app.route("/")
@login_required
def index():
    return render_template("index.html")


# MARK: - Login

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_error_template("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_error_template("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_error_template("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# MARK: - Collections

@app.route("/collections")
@login_required
def getCollections():
    collections = db.execute("SELECT * from collections WHERE user_id = ?", session["user_id"])
    response = jsonify(success=True, collections=collections)
    response.status_code = 200
    return response

@app.route("/deleteCollection", methods=["POST"])
@login_required
def deleteCollection():

    id = request.form.get("id")
    if not id:
        return "General Error", 500

    db.execute("DELETE FROM collections WHERE id = ?", id)
    db.execute("DELETE FROM cards WHERE collection_id = ?", id)

    response = jsonify(success=True)
    response.status_code = 200
    return response

@app.route("/createCollection", methods=["POST"])
@login_required
def createCollection():
    name = request.form.get("name")
    if not name:
        return "Must provide a collection name", 403

    id = db.execute("INSERT INTO collections (name, user_id) VALUES(?, ?)", name, session["user_id"])

    newCollection = db.execute("SELECT * from collections where id = ?", id)
    if len(newCollection) == 0:
        return "General Error", 500

    newCollection = newCollection[0]

    response = jsonify(success=True, newCollection=newCollection)
    response.status_code = 200
    return response

@app.route("/collection")
@login_required
def collection():
    id = request.args.get("id")
    collections = db.execute("SELECT * FROM collections WHERE id = ?", id)

    if len(collections) == 0:
        return render_error_template("General error", 500)

    collection = collections[0]

    return render_template("collection.html", collection=collection)


# MARK: - Cards

@app.route("/cards")
@login_required
def getCards():
    collection_id = request.args.get("collection_id")

    cards = db.execute("SELECT * FROM cards WHERE collection_id = ?", collection_id)

    response = jsonify(success=True, cards=cards)
    response.status_code = 200
    return response

@app.route("/deleteCard", methods=["POST"])
@login_required
def deleteCard():
    id = request.form.get("id")

    if not id:
        return "General error - no card id", 500

    db.execute("DELETE FROM cards WHERE id = ?", id)

    response = jsonify(success=True)
    response.status_code = 200
    return response


@app.route("/createCard", methods=["POST"])
@login_required
def createCard():
    title = request.form.get("title")
    content = request.form.get("content")
    collection_id = request.form.get("collection_id")

    if not title:
        return "Must provide a title", 403
    if not content:
        return "Must provide content", 403
    if not collection_id:
        return "General error", 500

    id = db.execute("INSERT INTO cards (title, content, collection_id) VALUES(?, ?, ?)", title, content, collection_id)

    newCard = db.execute("SELECT * from cards where id = ?", id)
    if len(newCard) == 0:
        "General Error", 500

    newCard = newCard[0]

    response = jsonify(success=True, newCard=newCard)
    response.status_code = 200
    return response


# MARK: - Registration

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        if not username:
            return render_error_template("must provide username")

        if not password:
            return render_error_template("must provide password")

        if not confirmation:
            return render_error_template("password has not been confirmed")

        if not password == confirmation:
            return render_error_template("passwords do not match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) > 0:
            return render_error_template("username is taken")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        return redirect("/")

    else:
        return render_template("register.html")


# MARK: - Password Change

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Register user"""
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        if not current_password:
            return render_error_template("must provide current password", 403)

        if not new_password:
            return render_error_template("must provide new password", 403)

        if not confirmation:
            return render_error_template("password has not been confirmed", 403)

        if not new_password == confirmation:
            return render_error_template("passwords do not match", 403)

        hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]

        if not check_password_hash(hash["hash"], current_password):
            return render_error_template("incorrect password", 403)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])
        return redirect("/")

    else:
        return render_template("change_password.html")
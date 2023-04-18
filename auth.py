import auth_middleware as middleware
from flask import redirect, render_template, request, session, Blueprint
from helpers import render_error_template, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from database import db

auth_bp = Blueprint('auth', __name__)

error_messages = {
    "invalid_credentials": "Invalid username or password - please try again",
    "username_taken": "username is taken",
    "incorrect_password": "incorrect password"
}


@auth_bp.route("/register", methods=["GET", "POST"])
@middleware.register_decorator
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) > 0:
            return render_error_template(error_messages["username_taken"])

        id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        session["user_id"] = id

        return redirect("/")

    else:
        return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@middleware.login_decorator
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_error_template(error_messages["invalid_credentials"], 401)

        session["user_id"] = rows[0]["id"]
        
        return redirect("/")
    else:
        return render_template("login.html")   


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


@auth_bp.route("/changePassword", methods=["GET", "POST"])
@login_required
@middleware.change_password_decorator
def changePassword():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")

    if request.method == "POST":
        hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]

        if not check_password_hash(hash["hash"], current_password):
            return render_error_template(error_messages["incorrect_password"])

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])
        return redirect("/")

    else:
        return render_template("change_password.html")
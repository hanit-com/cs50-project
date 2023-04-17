from flask import redirect, render_template, request, session, Blueprint
from helpers import render_error_template, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_error_template("must provide username", 403)

        elif not request.form.get("password"):
            return render_error_template("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_error_template("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")   


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
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

        id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        session["user_id"] = id

        return redirect("/")

    else:
        return render_template("register.html")


@auth_bp.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
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
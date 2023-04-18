from flask import request
from helpers import render_error_template
from functools import wraps
import re


error_messages = {
    "missing_username": "Please provide a username",
    "missing_password": "Please provide a password",
    "missing_current_password": "Please provide current password",
    "missing_new_password": "Please provide new password",
    "missing_password_confirmation": "Please provide a password confirmation",
    "username_too_short": "Username must be at least 5 characters long",
    "password_too_short": "Password must be at least 8 characters long",
    "username_no_letter": "Please include at least one letter in username",
    "username_no_digit": "Please include at least one digit in username",
    "password_no_letter": "Please include at least one letter in password",
    "password_no_digit": "Please include at least one digit in password",
    "passwords_do_not_match": "Passwords do not match. Please try again",
}


def validate_password(password):
    if not password:
        return error_messages["missing_password"]

    if len(password) < 8:
        return error_messages["password_too_short"]

    if not re.search("[a-zA-Z]", password):
        return error_messages["password_no_letter"]

    if not re.search("[0-9]", password):
        return error_messages["password_no_digit"]


# Login


def login_decorator(handler):
    def login_wrapper(*args, **kwargs):
        error_message = login_middleware()

        if error_message:
            return render_error_template(error_message, 401)
        
        return handler(*args, **kwargs)

    return login_wrapper


def login_middleware():
    if request.method != "POST":
        return

    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        return error_messages["missing_username"]

    elif not password:
        return error_messages["missing_password"]
    

# Register


def register_decorator(handler):
    @wraps(handler)
    def register_wrapper(*args, **kwargs):
        error_message = register_middleware()
        
        if error_message:
            return render_error_template(error_message)

        return handler(*args, **kwargs)

    return register_wrapper


def register_middleware():
    if request.method != "POST":
        return

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    password_error = validate_password(password)
    if password_error:
        return password_error

    if not username:
        return error_messages["missing_username"]

    if not confirmation:
        return error_messages["missing_password_confirmation"]

    if len(username) < 5:
        return error_messages["username_too_short"]

    if not re.search("[a-zA-Z]", username):
        return error_messages["username_no_letter"]

    if not re.search("[0-9]", username):
        return error_messages["username_no_digit"]

    if not password == confirmation:
        return error_messages["passwords_do_not_match"]


# Change Password


def change_password_decorator(handler):
    def password_wrapper(*args, **kwargs):
        error_message = change_password_middleware()

        if error_message:
            return render_error_template(error_message)
        
        return handler(*args, **kwargs)

    return password_wrapper


def change_password_middleware():
    if request.method != "POST":
        return

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirmation = request.form.get("confirmation")

    password_error = validate_password(new_password)
    if password_error:
        return password_error

    if not current_password:
        return error_messages["missing_current_password"]

    if not confirmation:
        return error_messages["missing_password_confirmation"]

    if not new_password == confirmation:
        return error_messages["passwords_do_not_match"]
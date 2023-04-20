from flask import request
from helpers import render_error_template
from functools import wraps
import re
from collections import deque
import time

call_history = {}

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
    'rate_limit_exceeded': 'Rate limit exceeded. Please try again in {seconds} seconds.'
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


def login_middleware(handler):
    def login_wrapper(*args, **kwargs):
        error_message = validate_login()

        if error_message:
            return render_error_template(error_message, 401)
        
        return handler(*args, **kwargs)

    return login_wrapper


def validate_login():
    if request.method != "POST":
        return

    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        return error_messages["missing_username"]

    elif not password:
        return error_messages["missing_password"]


def rate_limited(max_calls=5, time_frame=60):
    def decorator(handler):
        def wrapper(*args, **kwargs):
            ip_address = request.remote_addr

            if ip_address not in call_history:
                call_history[ip_address] = deque()
            
            queue = call_history[ip_address]
            current_time = time.time()
            
            while len(queue) > 0 and current_time - queue[0] > time_frame:
                queue.popleft()
            
            if len(queue) > max_calls:
                time_passed = current_time - queue[0]
                time_to_wait = int(time_frame - time_passed)
                error_message = error_messages['rate_limit_exceeded'].format(seconds=time_to_wait)
                return error_message, 429

            queue.append(current_time)

            return handler(*args, **kwargs)

        return wrapper

    return decorator


# Register


def register_middleware(handler):
    @wraps(handler)
    def register_wrapper(*args, **kwargs):
        error_message = validate_register()
        
        if error_message:
            return render_error_template(error_message)

        return handler(*args, **kwargs)

    return register_wrapper


def validate_register():
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


def change_password_middleware(handler):
    def password_wrapper(*args, **kwargs):
        error_message = validate_change_password()

        if error_message:
            return render_error_template(error_message)
        
        return handler(*args, **kwargs)

    return password_wrapper


def validate_change_password():
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
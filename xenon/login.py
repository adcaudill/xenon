import secrets
import time

from flask import make_response, redirect, request, url_for

from .template import render_template

LOGIN_FORM_HTML = """
    <div style="margin-bottom:10px;"><a href="/" class="back-link">&larr; Back to Home</a></div>
    <h1>Login</h1>
    <div style="display: flex; justify-content: center;">
        <form method="post" style="display: flex; flex-direction: column; gap: 16px; max-width: 350px; width: 100%;">
            <div>
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" style="width: 100%;">
            </div>
            <div>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" style="width: 100%;">
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
    <div style="margin-top:18px; text-align:center;">
        <a href="/reset" class="back-link">Forgot your password?</a>
    </div>
"""


def login_get():
    # Render a simple login form
    return render_template("Login", LOGIN_FORM_HTML)


def login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Simulate timing side-channel for valid usernames
    # this simulates a delay for valid usernames to demonstrate timing attacks
    # in a real-world scenario, this would be a security risk
    if username in ["admin@example.com", "test@example.com"]:
        time.sleep(0.2)

    valid = (username == "admin@example.com" and password == "admin") or (
        username == "test@example.com" and password == "test"
    )
    if valid:
        response = redirect(url_for("index"))
        session_value = secrets.token_hex(16)
        response.set_cookie("session", session_value, httponly=True, samesite="Lax")
        return response

    error_html = """
        <div class='alert-error'>
            <strong>Login Failed:</strong> Invalid username or password.
        </div>
    """

    html = render_template("Login", LOGIN_FORM_HTML + error_html)
    return make_response(html, 401)

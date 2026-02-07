import time

from flask import request

from .template import render_template

RESET_FORM_HTML = """
    <div style="margin-bottom:10px;"><a href="/login" class="back-link">&larr; Back to Login</a></div>
    <h1>Reset Password</h1>
    <div style="display: flex; justify-content: center;">
        <form method="post" style="display: flex; flex-direction: column; gap: 16px; max-width: 350px; width: 100%;">
            <div>
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" style="width: 100%;">
            </div>
            <button type="submit">Reset Password</button>
        </form>
    </div>
"""


def reset_get():
    return render_template("Reset Password", RESET_FORM_HTML)


def reset_post():
    username = request.form.get("username", "")
    if username in ["admin@example.com", "test@example.com"]:
        time.sleep(0.2)
        info_html = """
            <div class='alert-info'>
                <strong>Reset Requested:</strong> If this account exists, a password reset link will be sent to your email.
            </div>
        """
        html = render_template("Reset Password", RESET_FORM_HTML + info_html)
        return html
    
    error_html = """
        <div class='alert-error'>
            <strong>Reset Failed:</strong> User not found.
        </div>
    """
    html = render_template("Reset Password", RESET_FORM_HTML + error_html)
    return html

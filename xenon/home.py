from flask import make_response


def set_demo_cookies(response):
    """
    Sets a variety of cookies with different security properties.
    Each cookie demonstrates a different combination of security flags.

    Cookies set:
    1. bare_cookie: No security flags.
    2. httponly_cookie: HttpOnly only.
    3. secure_cookie: Secure only.
    4. secure_httponly_cookie: Secure + HttpOnly.
    5. lax_cookie: Secure + HttpOnly + SameSite=Lax.
    6. strict_cookie: Secure + HttpOnly + SameSite=Strict.
    7. none_cookie: Secure + HttpOnly + SameSite=None.
    8. expiring_cookie: Secure + HttpOnly + SameSite=Lax + expires in 1 hour.
    9. path_cookie: Secure + HttpOnly + SameSite=Lax + path restricted.
    10. domain_cookie: Secure + HttpOnly + SameSite=Lax + domain restricted.
    """
    # 1. Bare cookie: no security controls
    response.set_cookie(
        "bare_cookie",
        "bare_value",
        # No additional flags
    )
    # 2. HttpOnly only
    response.set_cookie("httponly_cookie", "httponly_value", httponly=True)
    # 3. Secure only
    response.set_cookie("secure_cookie", "secure_value", secure=True)
    # 4. HttpOnly + Secure
    response.set_cookie(
        "secure_httponly_cookie", "secure_httponly_value", httponly=True, secure=True
    )
    # 5. HttpOnly + Secure + SameSite=Lax
    response.set_cookie(
        "lax_cookie", "lax_value", httponly=True, secure=True, samesite="Lax"
    )
    # 6. HttpOnly + Secure + SameSite=Strict
    response.set_cookie(
        "strict_cookie", "strict_value", httponly=True, secure=True, samesite="Strict"
    )
    # 7. HttpOnly + Secure + SameSite=None (must be Secure)
    response.set_cookie(
        "none_cookie", "none_value", httponly=True, secure=True, samesite="None"
    )
    # 8. Cookie with expiration (max-age)
    response.set_cookie(
        "expiring_cookie",
        "expiring_value",
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    # 9. Cookie with path restriction
    response.set_cookie(
        "path_cookie",
        "path_value",
        path="/",
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    # 10. Cookie with domain restriction
    response.set_cookie(
        "domain_cookie",
        "domain_value",
        domain="xenon.example.com",
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    return response


def index():
    """
    Returns the home page and sets a variety of cookies with different security properties.
    """
    from .template import render_template

    html = render_template("Xenon Vulnerability Simulation Service", get_home_content())
    response = make_response(html)
    response = set_demo_cookies(response)
    return response


def get_home_content():
    return """
    <h1>Xenon Vulnerability Simulation Service</h1>
    <p>
        Welcome to <strong>Xenon</strong>, a test service designed to simulate vulnerabilities in a safe and controlled environment.
        This application is used for testing security scanners and tools with realistic, but non-exploitable, responses.
    </p>
    <div class="notice">
        <strong>Notice:</strong> All vulnerabilities in this service are simulated. No real security risks exist, and no sensitive data is present. Use this system for safe, realistic security testing and training.
    </div>
    <div class="links" style="margin-top:32px;">
        <h2 style="font-size:1.1em; margin-bottom:10px;">Explore Xenon</h2>
        <ul style="list-style:none; padding:0;">
            <li><a href="/login" style="text-decoration:none; font-weight:bold;">Login Page</a></li>
            <li><a href="/search" style="text-decoration:none; font-weight:bold;">Search Page</a></li>
            <li><a href="/ping" style="text-decoration:none; font-weight:bold;">Ping Page</a></li>
        </ul>
    </div>
    """

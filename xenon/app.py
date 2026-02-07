import os

from flask import Flask, send_from_directory
from xenon.home import index
from xenon.login import login_get, login_post
from xenon.ping import ping_get, ping_post
from xenon.reset import reset_get, reset_post
from xenon.search import search_get, search_post

app = Flask(__name__)


app.add_url_rule("/", view_func=index)

app.add_url_rule("/search", view_func=search_get, methods=["GET"])
app.add_url_rule("/search", view_func=search_post, methods=["POST"])

app.add_url_rule("/ping", view_func=ping_get, methods=["GET"])
app.add_url_rule("/ping", view_func=ping_post, methods=["POST"])


# Login page routes
app.add_url_rule("/login", view_func=login_get, methods=["GET"])
app.add_url_rule("/login", view_func=login_post, methods=["POST"])

# Reset Password page routes
app.add_url_rule("/reset", view_func=reset_get, methods=["GET"])
app.add_url_rule("/reset", view_func=reset_post, methods=["POST"])


@app.route("/phpinfo.php")
def phpinfo():
    resources_dir = os.path.join(os.path.dirname(__file__), "resources")
    response = send_from_directory(resources_dir, "phpinfo.html")
    response.headers["X-Powered-By"] = "PHP/5.0.4"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

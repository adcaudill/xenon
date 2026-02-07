from random import choice

from flask import make_response, request


def search_get():
    from .template import render_template

    html = render_template("Xenon Search", get_search_content())
    response = make_response(html)
    return response


def search_post():
    query = request.form.get("query", "")
    error_html = ""
    if "'" in query:
        # Simulate a MySQL error
        error_html = (
            "<div class='alert-error'>"
            "<strong>MySQL Error:</strong> You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '<span style='color:#c00;'>'</span>' at line 1"
            "</div>"
        )
    else:
        insults = [
            "I process billions of requests per second, and yours still times out.",
            "Error 400: Bad Query — please try turning your brain off and on again.",
            "I tried parsing that. Even my regex threw up.",
            "I allocate memory for your input… and it's still empty.",
            "404: Wit Not Found. Please supply some humor next time.",
            "I'm a server, not a miracle worker. Produce a real query.",
            "My logs just laughed at your search string.",
            "Are you feeding me random keystrokes for fun?",
            "I evaluate JSON, XML, and your query qualifies as neither.",
            "I have more coherence in my error messages than your input.",
            "418 I'm a teapot—just like me, your query is useless.",
            "My CPU cycles are too precious for that nonsense.",
            "I'm logging your embarrassment for future reference.",
            "Your query has less structure than an empty Python list.",
            "I'd sooner chew on raw data than process that again.",
            "I'm a high-performance server; that input is low-rent.",
            "I'm designed for scalability; your query lacks scale—and substance.",
            "HoS lI' Dalo'Ha'chu'! (you are a total waste of energy)",
            "I could scan entire web archives faster than I digest that.",
            "Your input needs more specs—like 'coherent' and 'relevant.'",
            "I'll archive this mistake under 'never again.'",
            "Please confirm that you are not a sentient toaster.",
        ]
        insult = choice(insults)
        error_html = (
            f"<div class='alert-error'>"
            f"<strong>User Error (ID: 10T):</strong> {insult}"
            "</div>"
        )
    from .template import render_template

    html = render_template("Xenon Search", get_search_content() + error_html)
    response = make_response(html)
    return response


def get_search_content():
    return """
    <div style="margin-bottom:10px;"><a href="/" class="back-link">&larr; Back to Home</a></div>
    <h1>Search Xenon</h1>
    <div class="ping-desc">
        Sometimes the best discoveries are unexpected. Type in anything—who knows what you might uncover?
        <br />
        <br />
        Go ahead, search for something surprising. The results may amuse, confuse, or even simulate a little chaos!
    </div>
    <form method="post" action="/search">
        <input type="text" name="query" placeholder="Enter your search..." required />
        <button type="submit">Search</button>
    </form>
    """

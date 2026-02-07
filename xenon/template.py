"""
Template rendering for Xenon web pages.
"""


def render_template(page_title, content_html):
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{page_title}</title>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background: #f7f7fa;
        color: #222;
        margin: 0;
        padding: 0;
      }}
      .container {{
        max-width: 600px;
        margin: 60px auto;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        padding: 32px;
      }}
      h1 {{ color: #3a3a7c; margin-bottom: 16px; }}
      .back-link {{
        color: #3a3a7c;
        text-decoration: none;
        font-size: 1em;
      }}
      .ping-desc {{
        margin-bottom: 18px;
        color: #444;
        font-size: 1.08em;
      }}
      form {{ margin-top: 24px; display: flex; align-items: center; gap: 12px; }}
      input[type=text], input[type=password] {{
        flex: 1;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #ccc;
        font-size: 1em;
      }}
      button {{
        padding: 10px 20px;
        border-radius: 4px;
        border: none;
        background: #3a3a7c;
        color: #fff;
        font-size: 1em;
        cursor: pointer;
      }}
      button:hover {{ background: #2a2a5c; }}
      .alert-error {{
        background: #ffeaea;
        border-left: 4px solid #c00;
        color: #222;
        padding: 12px;
        margin-top: 24px;
        border-radius: 4px;
      }}
      .alert-info {{
        background: #f0f8ff;
        border-left: 4px solid #3a3a7c;
        color: #222;
        padding: 12px;
        margin-top: 24px;
        border-radius: 4px;
      }}
      @media (prefers-color-scheme: dark) {{
        body {{ background: #181a20; color: #f5f7fa; }}
        .container {{ background: #232635; box-shadow: 0 2px 8px rgba(0,0,0,0.25); }}
        h1 {{ color: #e0e6ff; }}
        input[type=text], input[type=password] {{ background: #232635; color: #f5f7fa; border: 1px solid #888; }}
        button {{ background: #23265c; color: #fff; }}
        button:hover {{ background: #3a3a7c; }}
        .back-link {{ color: #6ec6ff; text-shadow: 0 1px 2px #232635; }}
        a {{ color: #6ec6ff; text-shadow: 0 1px 2px #232635; }}
        .ping-desc {{ color: #b8c7e0; }}
        .alert-error {{
          background: #2a1a1a;
          border-left: 4px solid #ff5c5c;
          color: #fff0f0;
        }}
        .alert-info {{
          background: #1a2230;
          border-left: 4px solid #e0e6ff;
          color: #e0e6ff;
        }}
      }}
    </style>
  </head>
  <body>
    <div class=\"container\">
      {content_html}
    </div>
    <footer style=\"text-align:center; margin-top:40px; color:#888; font-size:0.95em;\">
      Copyright &copy; <a href=\"https://adamcaudill.com\">Adam Caudill</a>
    </footer>
  </body>
</html>
"""

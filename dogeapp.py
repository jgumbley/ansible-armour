#!/usr/bin/env python

import random

from flask import Flask
from jinja2 import Template

app = Flask(__name__)

# A good generator is http://dogr.io
doge_images = [
    "http://i.imgur.com/631sWMX.jpg",
    "http://i.imgur.com/JXp9EeV.jpg",
    "http://i.imgur.com/nQ8BIC4.jpg",
    "http://i.imgur.com/EZ9t65z.png",
]


@app.route("/doges")
def doge():
    body = """
        <H1>Doge Application Entry</H1>
        <img src="{doge_image}">
    """.format(doge_image=random.choice(doge_images))

    return govuk_template_of_dubious_utility.render(pageTitle="Hello", content=body, assetPath="static/")

govuk_template_of_dubious_utility = Template("""
<!DOCTYPE html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>{{ pageTitle }}</title>
  </head>

  <body>

    {{ content|safe }}

    <footer class="group js-footer" id="footer" role="contentinfo">
            <p>All rights disavowed</p>
    </footer>
  </body>
</html>

""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=False)


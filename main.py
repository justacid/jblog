import argparse
import os

import flask
import flask_login
import jinja2

import editor
import login
import pages
import util


app = flask.Flask(__name__)
app.register_blueprint(pages.pages)
app.register_blueprint(login.login_pages)
app.register_blueprint(editor.editor_pages)
app.jinja_env.globals["fdate"] = util.js_format_datetime

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_pages.login_page"

# Development settings
app.config.update(
    DEBUG = True,
    APPLICATION_ROOT = "/",
    SECRET_KEY = b"TheNotSoSecretDevKey"
)

# Overwrite default dev settings with production settings.
# You must make sure this file is *not* checked into git!
app.config.from_pyfile("config.cfg", silent=True)


# Generic top-level 404, needed since the pages routes only
# handle 404 errors within the pages blueprint itself
@app.errorhandler(404)
def page_not_found(err):
    return flask.render_template("404.html"), 404


@login_manager.user_loader
def user_loader(user_id):
    return login.load_user(user_id)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=5000)
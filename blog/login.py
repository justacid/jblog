from flask import Blueprint, redirect, url_for
from flask import render_template, request, abort
import flask_login
from urllib.parse import urlparse, urljoin
from werkzeug.security import check_password_hash

from . import database as db


login_pages = Blueprint(
    "login_pages", __name__, template_folder="templates", static_folder="static")


def load_user(user_id):
    with db.session_context() as session:
        user = session.query(db.User).get(user_id)
        if user is None:
            return
        return user


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@login_pages.route("/login", methods=["GET", "POST"])
def login_page():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("pages.index_page"))

    if request.method == "GET":
        return render_template("login.html")

    with db.session_context() as session:
        username = request.form["username"]
        user = session.query(db.User).filter(db.User.username == username).first()

        if user and check_password_hash(user.pw_hash, request.form["password"]):
            next_page = request.args.get("next")
            if next_page and not is_safe_url(next_page):
                return abort(400)

            flask_login.login_user(user)
            return redirect(next_page or url_for("pages.index_page"))

    return render_template("login.html", login_failed=True)


@login_pages.route("/logout")
def logout_page():
    if flask_login.current_user.is_authenticated:
        flask_login.logout_user()
    return redirect(url_for("pages.index_page"))
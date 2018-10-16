from datetime import datetime

from flask import Blueprint
from flask import render_template, request, abort
import flask_login

import database as db


editor_pages = Blueprint(
    "editor", __name__, template_folder="templates", static_folder="static")


def insert_tags_for_post(session, tags, post_id):
    if tags == "Tag1, Tag2":
        return

    for tag_text in [t.strip() for t in tags.split(",")]:
        tag = session.query(db.Tag).filter(db.Tag.tag == tag_text).first()
        if not tag:
            tag = db.Tag(tag=tag_text)
            session.add(tag)
            session.flush()
        session.add(db.Post2Tag(post_id=post_id, tag_id=tag.rowid))


@editor_pages.route("/edit/new", methods=["GET", "POST"])
@flask_login.login_required
def new_post_page():
    post_data = {
        "title": "New Post",
        "text": "# New post\n\nEnter a new post here...",
        "published": datetime.utcnow()
    }

    if request.method == "GET":
        return render_template(
            "editor.html", post=db.Post(**post_data), tags="Tag1, Tag2", enable_save=True)

    tags = request.form["tags"]
    post_data["title"] = request.form["title"]
    post_data["text"] = request.form["post"]

    with db.session_context() as session:
        post = db.Post(**post_data)
        session.add(post)
        session.flush()
        insert_tags_for_post(session, tags, post.rowid)

    return render_template("editor.html", post=post, tags=tags, post_saved=True)


@editor_pages.route("/edit/id/<int:post_id>", methods=["GET", "POST"])
def edit_post_page(post_id):
    if request.method == "GET":
        with db.session_context() as session:
            post = session.query(db.Post).get(post_id)
            if post is None:
                abort(404)

            tags = session.query(db.Tag).join(
                db.Post2Tag, db.Tag.rowid == db.Post2Tag.tag_id).filter(
                    db.Post2Tag.post_id == post_id).all()

            tags_text = ", ".join([t.tag for t in tags])
            return render_template(
                "editor.html", post=post, tags=tags_text, enable_save=True)

    with db.session_context() as session:
        post = session.query(db.Post).get(post_id)
        if post is None:
            abort(404)

        tags = request.form["tags"]
        post.title = request.form["title"]
        post.text = request.form["post"]
        post.last_modified = datetime.utcnow()

        session.query(db.Post2Tag).filter(db.Post2Tag.post_id == post_id).delete()
        insert_tags_for_post(session, tags, post.rowid)

        return render_template(
            "editor.html", post=post, tags=tags, enable_save=True, post_saved=True)
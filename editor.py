from datetime import datetime

from flask import Blueprint
from flask import render_template, request, abort
import flask_login

import database as db


editor_pages = Blueprint(
    "editor", __name__, template_folder="templates", static_folder="static")


@editor_pages.route("/edit/new", methods=["GET", "POST"])
@flask_login.login_required
def new_post_page():
    if request.method == "GET":
        post_data = {
            "title": "New Post",
            "text": "# New post\n\nEnter a new post here...",
            "published": datetime.utcnow() 
        }
        post = db.Post(**post_data)
        return render_template("editor.html", post=post, tags="Tag1, Tag2", enable_save=True)

    tags = request.form["tags"]
    post_data = {
        "title": request.form["title"],
        "text": request.form["post"],
        "published": datetime.utcnow()
    }

    with db.session_context() as session:
        post = db.Post(**post_data)
        session.add(post)
        session.flush()

        if tags != "Tag1, Tag2":
            for tag_text in [t.strip() for t in tags.split(",")]:
                tag = session.query(db.Tag).filter(db.Tag.tag == tag_text).first()
                if not tag:
                    tag = db.Tag(tag=tag_text)
                    session.add(tag)
                    session.flush()
                session.add(db.Post2Tag(post_id=post.rowid, tag_id=tag.rowid))

    return render_template("editor.html", post=post, tags=tags, post_saved=True)
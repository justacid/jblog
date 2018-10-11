from collections import defaultdict
import datetime

from flask import Flask, render_template, request, abort
from werkzeug.contrib.atom import AtomFeed

import database as db


app = Flask(__name__)


@app.route("/")
def index_page():
    with db.session_context() as session:
        posts = session.query(db.Post).order_by(db.Post.published.desc()).limit(10)
        tags = session.query(db.Tag).join(
            db.Post2Tag, db.Tag.rowid == db.Post2Tag.tag_id).filter(
                db.Post2Tag.post_id == posts[0].rowid).all()
        return render_template("index.html", post=posts[0], older_posts=posts, tags=tags)


@app.route("/post/id/<int:post_id>")
def post_page(post_id):
    with db.session_context() as session:
        post = session.query(db.Post).get(post_id)
        posts = session.query(db.Post).order_by(db.Post.published.desc()).limit(10)
        tags = session.query(db.Tag).join(
            db.Post2Tag, db.Tag.rowid == db.Post2Tag.tag_id).filter(
                db.Post2Tag.post_id == post_id).all()
        if post is None:
            abort(404)
        return render_template("post.html", post=post, older_posts=posts, tags=tags)


@app.route("/feed")
def feed_page():
    with db.session_context() as session:
        posts = session.query(db.Post).order_by(db.Post.published).limit(10)
        feed = AtomFeed(title="Recent Posts", feed_url=request.url, url=request.url_root)

        for post in posts:
            updated = post.published if post.last_modified is None else post.last_modified
            feed.add(post.title, post.html, content_type="html",
                    url="{0}/post?id={1}".format(request.url_root, post.rowid),
                    updated=updated, published=post.published)

        return feed.get_response()


@app.route("/archive")
@app.route("/archive/tag/<string:tag>")
def archive_page(tag=None):
    with db.session_context() as session:
        if tag:
            posts = session.query(db.Post).join(
                db.Post2Tag, db.Post.rowid == db.Post2Tag.post_id).join(
                    db.Tag, db.Tag.rowid == db.Post2Tag.tag_id).filter(
                        db.Tag.tag == tag).all()
            if not posts:
                abort(404)
        else:
            posts = session.query(db.Post).order_by(db.Post.published).all()
        tags = session.query(db.Tag).all()
        return render_template("archive.html", tags=tags, posts=posts, tag_filter=tag)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
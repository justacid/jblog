from flask import Flask, render_template, request, abort
from post import Post, load_posts, posts_by_year
from werkzeug.contrib.atom import AtomFeed
import datetime


app = Flask(__name__)


@app.route("/")
def index():
    posts = load_posts("static/posts/")
    return render_template("index.html", newest=posts[0], posts=posts_by_year(posts))


@app.route("/post", methods=["GET"])
def render_post():
    post_id = request.args["id"]
    posts = load_posts("static/posts/")

    for post in posts:
        if post.post_id == post_id:
            break
    else:
        abort(404)

    return render_template("post.html", post=post, posts=posts_by_year(posts))


@app.route("/feed")
def feed():
    posts = load_posts("static/posts/")
    feed = AtomFeed(title="Recent Articles", feed_url=request.url, url=request.url_root)

    for post in posts[:min(10, len(posts))]:
        feed.add(post.title, post.html, content_type="html",
                 url="{0}/post?id={1}".format(request.url_root, post.post_id),
                 updated=post.date, published=post.date)

    return feed.get_response()


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")

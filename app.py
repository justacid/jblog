from flask import Flask, render_template, request, abort
from post import BlogPost, load_blog_posts


app = Flask(__name__)


@app.route("/")
def index():
    posts = load_blog_posts("static/posts/")
    return render_template("index.html", posts=posts)


@app.route("/post", methods=["GET"])
def render_post():
    identifier = request.args["id"]
    try:
        with open(f"static/posts/{identifier}.md", "r") as pf:
            post = BlogPost(identifier, pf)
        return render_template("post.html", post=post)
    except FileNotFoundError:
        abort(404)


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()


from flask import Flask, render_template
from routes import pages


app = Flask(__name__)
app.register_blueprint(pages)

app.config.update(
    DEBUG=True,
    APPLICATION_ROOT="/",
    SECRET_KEY=b"TheNotSoSecretDevKey"
)

# Overwrite default dev settings with production settings.
# You must make sure this file is *not* checked into git!
app.config.from_pyfile("config.cfg", silent=True)


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
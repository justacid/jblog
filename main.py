import argparse
import os

from flask import Flask, render_template
from routes import pages


app = Flask(__name__)
app.register_blueprint(pages)

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
    return render_template("404.html"), 404


def create_deploy_config():
    with open("config.cfg", "w") as cfg:
        cfg.writelines([
            "DEBUG = False\n",
            "APPLICATION_ROOT = '/'\n",
            "SECRET_KEY = {0}\n".format(os.urandom(16))
        ])


def main(args):
    if args.create_deploy_config:
        create_deploy_config()
        return
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=5000, type=int)
    parser.add_argument("--create-deploy-config", action="store_true")

    main(parser.parse_args())
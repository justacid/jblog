import argparse
import datetime
import getpass
import os
import textwrap

from werkzeug.security import generate_password_hash

from blog import database as db


def create_database():
    if os.path.isfile("blog.db"):
        print("A database already exists, overwrite? [y/N]")
        choice = input(">> ").lower().strip()
        if choice in ["", "n", "no"]:
            print("Did not write a new database!")
            return
        os.remove("blog.db")

    db._Base.metadata.create_all(db._engine)

    # add some dummy data
    with db.session_context() as session:
        timestamp = datetime.datetime.utcnow()
        text = textwrap.dedent("""\
            ## Dolor sit amet
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.""")
        session.add(db.Post(title="Lorem Ipsum", text=text, published=timestamp))
        session.add(db.Tag(tag="Lorem"))
        session.add(db.Post2Tag(post_id=1, tag_id=1))

    print("Success: Created new database.")


def delete_user_account(username):
    with db.session_context() as session:
        user = session.query(db.User).filter(db.User.username == username).first()
        if not user:
            print("Error: Account '{0}' does not exist.".format(username))
            return

        print("Really delete '{0}'? [y/N]".format(username))
        choice = input(">> ").lower().strip()
        if choice in ["", "n", "no"]:
            print("Did not delete user!")
            return

        session.delete(user)

    print("Success: Deleted user '{0}'.".format(username))


def create_user_account(username):
    with db.session_context() as session:
        exists = session.query(db.User).filter(db.User.username == username).first()
        if exists:
            print("Error: Account '{0}' already exists.".format(username))
            return

        try:
            password = getpass.getpass("Set a password: ")
        except getpass.GetPassWarning:
            print("Error: Could not safely set password.")
            return

        pw_hash = generate_password_hash(password)
        new_user = db.User(username=username, pw_hash=pw_hash, is_admin=1)
        session.add(new_user)

    print("Success: Added new user '{0}'.".format(username))


def create_deploy_config():
    if os.path.isfile("config.cfg"):
        print("A production config already exists, overwrite? [y/N]")
        choice = input(">> ").lower().strip()
        if choice in ["", "n", "no"]:
            print("Did not write a new config!")
            return

    with open("config.cfg", "w") as cfg:
        cfg.writelines([
            "DEBUG = False\n",
            "APPLICATION_ROOT = '/'\n",
            "SECRET_KEY = {0}\n".format(os.urandom(16))
        ])
    print("Success: New config written.")


def main(args):
    if args.create_deploy_config:
        create_deploy_config()
    if args.create_user_account:
        create_user_account(args.create_user_account)
    if args.delete_user_account:
        delete_user_account(args.delete_user_account)
    if args.create_database:
        create_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create-deploy-config", action="store_true", 
        help="Generates a new production config. Only run once!")
    parser.add_argument(
        "--create-user-account", metavar="USERNAME",
        help="Create a new account for given username.")
    parser.add_argument(
        "--delete-user-account", metavar="USERNAME",
        help="Delete the account of a given username.")
    parser.add_argument(
        "--create-database", action="store_true",
        help="Create a new empty database with the required schema.")
    main(parser.parse_args())
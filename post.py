from markdown.extensions.toc import TocExtension
from collections import defaultdict
from pathlib import Path
import datetime
import markdown
import os


class Post:

    def __init__(self, post_id, file_object):
        self.post_id = post_id

        _, date_str = self.post_id.split("_")
        self.date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        lines = file_object.readlines()
        self.title = lines[0][1:] if lines[0].startswith("#") else "Acid's Blog"

        md = markdown.Markdown(extensions=[
            TocExtension(baselevel=2, marker=""),
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite"
        ])

        self.html = md.convert("".join(lines[1:]))
        self.toc = md.toc


def load_posts(root_path):
    posts = []
    root_path = Path(root_path)

    for filename in os.listdir(root_path):
        with open(root_path / filename, "r") as post_file:
            post_id, _ = filename.split(".")
            posts.append(Post(post_id, post_file))

    return sorted(posts, reverse=True, key=lambda x: x.date)


def posts_by_year(posts):
    by_year = defaultdict(list)
    for post in posts:
        by_year[post.date.year].append(post)

    return by_year

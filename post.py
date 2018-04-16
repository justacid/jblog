from markdown.extensions.toc import TocExtension
from pathlib import Path
import markdown
import os


class BlogPost:

    def __init__(self, identifier, file_object):
        self.identifier = identifier

        lines = file_object.readlines();
        self.title = lines[0][1:] if lines[0].startswith("#") else "Acid's Blog"

        md = markdown.Markdown(extensions=[
            TocExtension(baselevel=2, marker=""),
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite"
        ])

        self.html = md.convert("".join(lines[1:]))
        self.toc = md.toc


def load_blog_posts(root_path):
    posts = []
    root_path = Path(root_path)

    for filename in os.listdir(root_path):
        with open(root_path / filename, "r") as pf:
            identifier = filename.split(".")[0]
            posts.append(BlogPost(identifier, pf))

    return posts

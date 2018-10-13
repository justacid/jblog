from contextlib import contextmanager

from flask_login import UserMixin
import markdown
from markdown.extensions.toc import TocExtension
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


_Base = declarative_base()
_engine = create_engine("sqlite:///blog.db")
_Session = sessionmaker(bind=_engine, expire_on_commit=False)


class Post(_Base):
    __tablename__ = "posts"

    rowid = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    published = Column(DateTime)
    last_modified = Column(DateTime)

    @property
    def html(self):
        md_converter = markdown.Markdown(extensions=[
            TocExtension(baselevel=2, marker=""),
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite"
        ])
        return md_converter.convert(self.text)

    @property
    def toc(self):
        md_converter = markdown.Markdown(extensions=[
            TocExtension(baselevel=2, marker=""),
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite"
        ])
        md_converter.convert(self.text)
        return md_converter.toc

    def __repr__(self):
        return "<Post(title='{0}', published='{1}', ...)>".format(
            self.title, self.published)


class Tag(_Base):
    __tablename__ = "tags"

    rowid = Column(Integer, primary_key=True)
    tag = Column(String)

    def __repr__(self):
        return "<Tag(tag='{0}')>".format(self.tag)


class Post2Tag(_Base):
    __tablename__ = "posts2tags"

    rowid = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    tag_id = Column(Integer)

    def __repr__(self):
        return "<Post2Tag(post_id='{0}', tag_id='{1}')>".format(
            self.post_id, self.tag_id)


class User(_Base, UserMixin):
    __tablename__ = "users"

    rowid = Column(Integer, primary_key=True)
    username = Column(String)
    pw_hash = Column(String)
    is_admin = Column(Integer)
    fullname = Column(String)

    @property
    def id(self):
        return str(self.rowid)

    def __repr__(self):
        return "<User(username='{0}', is_admin='{1}')>".format(
            self.username, self.is_admin)


@contextmanager
def session_context():
    session = _Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
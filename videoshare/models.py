from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class Video(db.Model):  # type: ignore
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self) -> str:
        return "<Video {}>".format(self.name)


class Folder(db.Model):  # type: ignore
    __tablename__ = "folders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self) -> str:
        return "<Folder {}>".format(self.name)

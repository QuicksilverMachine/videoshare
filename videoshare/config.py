import os


class Config:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///../videoshare.sqlite3",
    )


class TestConfig(Config):
    TESTING = True
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///../videoshare-test.sqlite3"

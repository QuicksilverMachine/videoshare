import os


class Config:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://videoshare:videoshare@localhost:5432/videoshare",
    )


class TestConfig(Config):
    TESTING = True
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/videoshare.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

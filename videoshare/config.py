import os


class Config:
    FLASK_DEBUG = os.getenv("DEBUG", True)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://videoshare:videoshare@localhost:5432/videoshare",
    )

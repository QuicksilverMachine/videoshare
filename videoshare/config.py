class Config:
    FLASK_DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///videoshare.db"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://videoshare:videoshare@localhost:5432/videoshare"
    )

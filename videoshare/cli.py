import logging

from flask.cli import AppGroup

from videoshare.models import Folder, Video, db

dev_cli = AppGroup("dev", help="Development commands")
logger = logging.getLogger(__name__)


@dev_cli.command("init-db", help="Initialize development database")  # type: ignore
def init_db() -> None:
    try:
        logger.info("Truncating existing data")
        db.session.query(Video).delete()
        db.session.query(Folder).delete()

        logger.info("Inserting test data")
        folder1 = Folder(name="folder1")
        folder2 = Folder(name="folder2")
        folder3 = Folder(name="folder3")
        video1 = Video(name="video1")
        video2 = Video(name="video2")
        video3 = Video(name="video3")

        db.session.add(folder1)
        db.session.add(video1)
        db.session.flush()

        folder2.parent_id = folder1.id
        folder3.parent_id = folder1.id

        db.session.add(folder1)
        db.session.add(folder2)
        db.session.add(folder3)
        db.session.flush()

        video2.parent_id = folder2.id
        video3.parent_id = folder2.id

        db.session.add(video2)
        db.session.add(video3)

        db.session.commit()
        logger.info("Database initialization successful")
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
        db.session.rollback()

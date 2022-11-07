from flask.cli import AppGroup

from videoshare.models import Folder, Video, db

dev_cli = AppGroup("dev", help="Development commands")


@dev_cli.command("init-db", help="Initialize development database")  # type: ignore
def init_db() -> None:
    try:
        db.session.query(Video).delete()  # type: ignore
        db.session.query(Folder).delete()  # type: ignore

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
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        db.session.rollback()
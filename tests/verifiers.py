from videoshare.models import Folder, Video


class Verifiers:
    def __init__(self):
        pass
        self.http_response = HttpResponseVerifier
        self.video = VideoVerifier
        self.folder = FolderVerifier


class HttpResponseVerifier:
    @staticmethod
    def status(response, status_code):
        assert response.status_code == status_code

    @staticmethod
    def data(response, expected):
        assert response.json == expected


class VideoVerifier:
    @staticmethod
    def saved(video_id):
        assert Video.query.filter_by(id=video_id).first() is not None

    @staticmethod
    def exists(video_id, parent_id):
        assert (
            Video.query.filter_by(id=video_id, parent_id=parent_id).first() is not None
        )


class FolderVerifier:
    @staticmethod
    def saved(folder_id):
        assert Folder.query.filter_by(id=folder_id).first() is not None

    @staticmethod
    def exists(folder_id, parent_id):
        assert (
            Folder.query.filter_by(id=folder_id, parent_id=parent_id).first()
            is not None
        )

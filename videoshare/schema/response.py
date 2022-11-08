from apiflask import Schema
from apiflask.fields import List, Nested, String


class StatusResponse(Schema):
    status = String()


class NodeResponse(Schema):
    id = String()
    name = String()
    type = String()
    parent_id = String()
    path = String()


class VideoResponse(NodeResponse):
    pass


class FolderResponse(NodeResponse):
    # noinspection PyTypeChecker
    contents = List(Nested(NodeResponse))

from apiflask import Schema
from apiflask.fields import Integer, List, Nested, String


class StatusResponse(Schema):
    status = String()


class NodeResponse(Schema):
    id = Integer()
    name = String()
    type = String()
    parent_id = String()
    path = String()


class VideoResponse(NodeResponse):
    pass


class FolderResponse(NodeResponse):
    # noinspection PyTypeChecker
    contents = List(Nested(NodeResponse))

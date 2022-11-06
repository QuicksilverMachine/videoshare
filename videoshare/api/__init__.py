from videoshare.api.explore import explore_blueprint
from videoshare.api.folder import folder_blueprint
from videoshare.api.status import status_blueprint
from videoshare.api.video import video_blueprint

routes = [
    explore_blueprint,
    status_blueprint,
    folder_blueprint,
    video_blueprint,
]

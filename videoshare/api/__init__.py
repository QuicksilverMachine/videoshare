from videoshare.api.explorer import explorer_blueprint
from videoshare.api.status import status_blueprint

routes = [
    explorer_blueprint,
    status_blueprint,
]

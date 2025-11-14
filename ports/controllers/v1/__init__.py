from litestar.router import Router

from .armor import ArmorController
from .material import MaterialController

router = Router(
    path="/api/v1",
    route_handlers=[ArmorController, MaterialController],
)

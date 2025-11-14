from litestar import Litestar
from ports.controllers.v1 import router

app = Litestar(route_handlers=[router])

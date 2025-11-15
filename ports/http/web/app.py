from litestar import Litestar
from ports.http.web.controllers.v1 import router

app = Litestar(route_handlers=[router])

from litestar import Litestar
from ports.http.web.v1.controllers import router

app = Litestar(route_handlers=[router])

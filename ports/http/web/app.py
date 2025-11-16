from config import config
from litestar import Litestar
from ports.http.web.v1.controllers import router

app = Litestar(route_handlers=[router], allowed_hosts=config.ALLOWED_HOSTS)

from config import config
from domain.error import DomainError
from litestar import Litestar
from litestar.config.cors import CORSConfig
from ports.http.web.exception_handlers import domain_handler
from ports.http.web.v1.controllers import router

cors = CORSConfig(allow_origins=config.ALLOWED_ORIGINS)

app = Litestar(
    route_handlers=[router],
    exception_handlers={DomainError: domain_handler},
    allowed_hosts=config.ALLOWED_HOSTS,
    cors_config=cors,
)

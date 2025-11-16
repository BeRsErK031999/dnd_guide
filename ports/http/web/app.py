from config import config
from domain.error import DomainError
from litestar import Litestar
from ports.http.web.exception_handlers import domain_handler
from ports.http.web.v1.controllers import router

app = Litestar(
    route_handlers=[router],
    exception_handlers={DomainError: domain_handler},
    allowed_hosts=config.ALLOWED_HOSTS,
)

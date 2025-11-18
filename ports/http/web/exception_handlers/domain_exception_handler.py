from domain.error import DomainError, DomainErrorStatus
from litestar import Request, Response
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def domain_handler(request: Request, exc: DomainError) -> Response:
    match exc.status:
        case DomainErrorStatus.NOT_FOUND:
            status = HTTP_404_NOT_FOUND
        case DomainErrorStatus.INVALID_DATA:
            status = HTTP_400_BAD_REQUEST
        case DomainErrorStatus.ACCESS:
            status = HTTP_403_FORBIDDEN
        case DomainErrorStatus.IDEMPOTENT:
            status = HTTP_400_BAD_REQUEST
        case DomainErrorStatus.POLICY:
            status = HTTP_403_FORBIDDEN
        case _:
            status = HTTP_500_INTERNAL_SERVER_ERROR
    return Response(
        content={
            "status_code": status,
            "detail": f"Validation failed for {request.method} {request.url.path}",
            "extra": [{"message": exc.msg}],
        },
        status_code=status,
    )

from litestar import get
from ports.http.web.v1.schemas.creature_size import ReadCreatureSizeSchema


@get("/creatures/sizes", tags=["creature"])
async def get_creature_sizes() -> ReadCreatureSizeSchema:
    return ReadCreatureSizeSchema.from_app()

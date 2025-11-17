from litestar import get
from ports.http.web.v1.schemas.creature_type import ReadCreatureTypeSchema


@get("/creatures/types", tags=["creature"])
async def get_creature_types() -> ReadCreatureTypeSchema:
    return ReadCreatureTypeSchema.from_domain()

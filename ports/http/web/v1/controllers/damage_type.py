from litestar import get
from ports.http.web.v1.schemas.damage_type import ReadDamageTypeSchema


@get("/damage-types", tags=["damage type"])
async def get_damage_types() -> ReadDamageTypeSchema:
    return ReadDamageTypeSchema.from_domain()

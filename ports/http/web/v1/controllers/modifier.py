from litestar import get
from ports.http.web.v1.schemas.modifier import ReadModifierSchema


@get("/modifiers", tags=["modifier"])
async def get_modifiers() -> ReadModifierSchema:
    return ReadModifierSchema.from_domain()

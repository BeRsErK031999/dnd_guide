from litestar import get
from ports.http.web.v1.schemas.weight import ReadWeightUnitSchema


@get("/weights/units", tags=["weight"])
async def get_weight_units() -> ReadWeightUnitSchema:
    return ReadWeightUnitSchema.from_app()

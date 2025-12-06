from litestar import get
from ports.http.web.v1.schemas.length import ReadLengthUnitSchema


@get("/lengths/units", tags=["length"])
async def get_length_units() -> ReadLengthUnitSchema:
    return ReadLengthUnitSchema.from_app()

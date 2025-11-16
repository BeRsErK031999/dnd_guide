from litestar import get
from ports.http.web.v1.schemas.coin import ReadPieceTypeSchema


@get("/coins/piece-types", tags=["coin"])
async def get_piece_types() -> ReadPieceTypeSchema:
    return ReadPieceTypeSchema.from_domain()

from litestar import get
from ports.http.web.v1.schemas.dice import ReadDiceTypeSchema


@get("/dices/types", tags=["dice"])
async def get_dice_types() -> ReadDiceTypeSchema:
    return ReadDiceTypeSchema.from_domain()

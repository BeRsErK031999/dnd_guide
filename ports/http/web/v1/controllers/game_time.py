from litestar import get
from ports.http.web.v1.schemas.game_time import ReadGameTimeUnitSchema


@get("/game-times/units", tags=["game time"])
async def get_game_time_units() -> ReadGameTimeUnitSchema:
    return ReadGameTimeUnitSchema.from_app()

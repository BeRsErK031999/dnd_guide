from uuid import UUID, uuid4

from application.dto.command.race import DeleteRaceCommand
from application.dto.query.race import RaceQuery, RacesQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import RaceUseCases, di_race_use_cases
from ports.http.web.v1.schemas.race import (
    CreateRaceSchema,
    ReadRaceSchema,
    UpdateRaceSchema,
)


class RaceController(Controller):
    path = "/races"
    tags = ["race"]

    dependencies = {"use_cases": Provide(di_race_use_cases, sync_to_thread=True)}

    @get("/{race_id:uuid}")
    async def get_race(self, race_id: UUID, use_cases: RaceUseCases) -> ReadRaceSchema:
        race = await use_cases.get_one.execute(RaceQuery(race_id=race_id))
        return ReadRaceSchema.from_app(race)

    @get()
    async def get_races(
        self, search_by_name: str | None, use_cases: RaceUseCases
    ) -> list[ReadRaceSchema]:
        query = RacesQuery(search_by_name=search_by_name)
        races = await use_cases.get_all.execute(query)
        return [ReadRaceSchema.from_app(race) for race in races]

    @post()
    async def create_race(
        self, data: CreateRaceSchema, use_cases: RaceUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{race_id:uuid}")
    async def update_race(
        self,
        race_id: UUID,
        data: UpdateRaceSchema,
        use_cases: RaceUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), race_id))

    @delete("/{race_id:uuid}")
    async def delete_race(self, race_id: UUID, use_cases: RaceUseCases) -> None:
        command = DeleteRaceCommand(user_id=uuid4(), race_id=race_id)
        await use_cases.delete.execute(command)

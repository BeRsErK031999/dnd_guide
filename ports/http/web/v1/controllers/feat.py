from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.feat import (
    CreateFeatCommand,
    DeleteFeatCommand,
    UpdateFeatCommand,
)
from application.dto.query.feat import FeatQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import FeatUseCases, di_feat_use_cases
from ports.http.web.v1.schemas.feat import (
    CreateFeatSchema,
    ReadFeatSchema,
    UpdateFeatSchema,
)


class FeatController(Controller):
    path = "/feats"
    tags = ["feat"]

    dependencies = {"use_cases": Provide(di_feat_use_cases, sync_to_thread=True)}

    @get("/{feat_id:uuid}")
    async def get_feat(self, feat_id: UUID, use_cases: FeatUseCases) -> ReadFeatSchema:
        feat = await use_cases.get_one.execute(FeatQuery(feat_id=feat_id))
        return ReadFeatSchema.from_domain(feat)

    @get()
    async def get_feats(self, use_cases: FeatUseCases) -> list[ReadFeatSchema]:
        feats = await use_cases.get_all.execute()
        return [ReadFeatSchema.from_domain(feat) for feat in feats]

    @post()
    async def create_feat(
        self, data: CreateFeatSchema, use_cases: FeatUseCases
    ) -> UUID:
        command = CreateFeatCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{feat_id:uuid}")
    async def update_feat(
        self,
        feat_id: UUID,
        data: UpdateFeatSchema,
        use_cases: FeatUseCases,
    ) -> None:
        command = UpdateFeatCommand(user_id=uuid4(), feat_id=feat_id, **asdict(data))
        await use_cases.update.execute(command)

    @delete("/{feat_id:uuid}")
    async def delete_feat(self, feat_id: UUID, use_cases: FeatUseCases) -> None:
        command = DeleteFeatCommand(user_id=uuid4(), feat_id=feat_id)
        await use_cases.delete.execute(command)

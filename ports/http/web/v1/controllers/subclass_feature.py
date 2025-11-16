from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.subclass_feature import (
    CreateSubclassFeatureCommand,
    DeleteSubclassFeatureCommand,
    UpdateSubclassFeatureCommand,
)
from application.dto.query.subclass_feature import SubclassFeatureQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    SubclassFeatureUseCases,
    di_subclass_feature_use_cases,
)
from ports.http.web.v1.schemas.subclass_feature import (
    CreateSubclassFeatureSchema,
    ReadSubclassFeatureSchema,
    UpdateSubclassFeatureSchema,
)


class SubclassFeatureController(Controller):
    path = "/subclass-features"
    tags = ["subclass feature"]

    dependencies = {
        "use_cases": Provide(di_subclass_feature_use_cases, sync_to_thread=True)
    }

    @get("/{feature_id:uuid}")
    async def get_feature(
        self, feature_id: UUID, use_cases: SubclassFeatureUseCases
    ) -> ReadSubclassFeatureSchema:
        feature = await use_cases.get_one.execute(
            SubclassFeatureQuery(feature_id=feature_id)
        )
        return ReadSubclassFeatureSchema.from_domain(feature)

    @get()
    async def get_features(
        self, use_cases: SubclassFeatureUseCases
    ) -> list[ReadSubclassFeatureSchema]:
        features = await use_cases.get_all.execute()
        return [ReadSubclassFeatureSchema.from_domain(feature) for feature in features]

    @post()
    async def create_feature(
        self, data: CreateSubclassFeatureSchema, use_cases: SubclassFeatureUseCases
    ) -> UUID:
        command = CreateSubclassFeatureCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{feature_id:uuid}")
    async def update_feature(
        self,
        feature_id: UUID,
        data: UpdateSubclassFeatureSchema,
        use_cases: SubclassFeatureUseCases,
    ) -> None:
        command = UpdateSubclassFeatureCommand(
            user_id=uuid4(), feature_id=feature_id, **asdict(data)
        )
        await use_cases.update.execute(command)

    @delete("/{feature_id:uuid}")
    async def delete_feature(
        self, feature_id: UUID, use_cases: SubclassFeatureUseCases
    ) -> None:
        command = DeleteSubclassFeatureCommand(user_id=uuid4(), feature_id=feature_id)
        await use_cases.delete.execute(command)

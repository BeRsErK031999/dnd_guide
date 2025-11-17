from dataclasses import asdict
from uuid import UUID, uuid4

from application.dto.command.class_feature import (
    CreateClassFeatureCommand,
    DeleteClassFeatureCommand,
    UpdateClassFeatureCommand,
)
from application.dto.query.class_feature import ClassFeatureQuery
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from ports.http.web.v1.providers.di_use_cases import (
    ClassFeatureUseCases,
    di_class_feature_use_cases,
)
from ports.http.web.v1.schemas.class_feature import (
    CreateClassFeatureSchema,
    ReadClassFeatureSchema,
    UpdateClassFeatureSchema,
)


class ClassFeatureController(Controller):
    path = "/class-features"
    tags = ["class feature"]

    dependencies = {
        "use_cases": Provide(di_class_feature_use_cases, sync_to_thread=True)
    }

    @get("/{feature_id:uuid}")
    async def get_feature(
        self, feature_id: UUID, use_cases: ClassFeatureUseCases
    ) -> ReadClassFeatureSchema:
        feature = await use_cases.get_one.execute(
            ClassFeatureQuery(feature_id=feature_id)
        )
        return ReadClassFeatureSchema.from_domain(feature)

    @get()
    async def get_features(
        self, filter_by_class_id: UUID, use_cases: ClassFeatureUseCases
    ) -> list[ReadClassFeatureSchema]:
        features = await use_cases.get_all.execute()
        return [ReadClassFeatureSchema.from_domain(feature) for feature in features]

    @post()
    async def create_feature(
        self, data: CreateClassFeatureSchema, use_cases: ClassFeatureUseCases
    ) -> UUID:
        command = CreateClassFeatureCommand(user_id=uuid4(), **asdict(data))
        return await use_cases.create.execute(command)

    @put("/{feature_id:uuid}")
    async def update_feature(
        self,
        feature_id: UUID,
        data: UpdateClassFeatureSchema,
        use_cases: ClassFeatureUseCases,
    ) -> None:
        command = UpdateClassFeatureCommand(
            user_id=uuid4(), feature_id=feature_id, **asdict(data)
        )
        await use_cases.update.execute(command)

    @delete("/{feature_id:uuid}")
    async def delete_feature(
        self, feature_id: UUID, use_cases: ClassFeatureUseCases
    ) -> None:
        command = DeleteClassFeatureCommand(user_id=uuid4(), feature_id=feature_id)
        await use_cases.delete.execute(command)

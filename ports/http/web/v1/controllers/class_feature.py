from uuid import UUID, uuid4

from application.dto.command.class_feature import DeleteClassFeatureCommand
from application.dto.query.class_feature import ClassFeatureQuery, ClassFeaturesQuery
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
        return ReadClassFeatureSchema.from_app(feature)

    @get()
    async def get_features(
        self, filter_by_class_id: UUID, use_cases: ClassFeatureUseCases
    ) -> list[ReadClassFeatureSchema]:
        query = ClassFeaturesQuery(filter_by_class_id=filter_by_class_id)
        features = await use_cases.get_all.execute(query)
        return [ReadClassFeatureSchema.from_app(feature) for feature in features]

    @post()
    async def create_feature(
        self, data: CreateClassFeatureSchema, use_cases: ClassFeatureUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{feature_id:uuid}")
    async def update_feature(
        self,
        feature_id: UUID,
        data: UpdateClassFeatureSchema,
        use_cases: ClassFeatureUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), feature_id))

    @delete("/{feature_id:uuid}")
    async def delete_feature(
        self, feature_id: UUID, use_cases: ClassFeatureUseCases
    ) -> None:
        command = DeleteClassFeatureCommand(user_id=uuid4(), feature_id=feature_id)
        await use_cases.delete.execute(command)

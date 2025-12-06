from uuid import UUID, uuid4

from application.dto.command.subclass_feature import DeleteSubclassFeatureCommand
from application.dto.query.subclass_feature import (
    SubclassFeatureQuery,
    SubclassFeaturesQuery,
)
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
        return ReadSubclassFeatureSchema.from_app(feature)

    @get()
    async def get_features(
        self, filter_by_subclass_id: UUID, use_cases: SubclassFeatureUseCases
    ) -> list[ReadSubclassFeatureSchema]:
        query = SubclassFeaturesQuery(filter_by_subclass_id=filter_by_subclass_id)
        features = await use_cases.get_all.execute(query)
        return [ReadSubclassFeatureSchema.from_app(feature) for feature in features]

    @post()
    async def create_feature(
        self, data: CreateSubclassFeatureSchema, use_cases: SubclassFeatureUseCases
    ) -> UUID:
        return await use_cases.create.execute(data.to_command(uuid4()))

    @put("/{feature_id:uuid}")
    async def update_feature(
        self,
        feature_id: UUID,
        data: UpdateSubclassFeatureSchema,
        use_cases: SubclassFeatureUseCases,
    ) -> None:
        await use_cases.update.execute(data.to_command(uuid4(), feature_id))

    @delete("/{feature_id:uuid}")
    async def delete_feature(
        self, feature_id: UUID, use_cases: SubclassFeatureUseCases
    ) -> None:
        command = DeleteSubclassFeatureCommand(user_id=uuid4(), feature_id=feature_id)
        await use_cases.delete.execute(command)

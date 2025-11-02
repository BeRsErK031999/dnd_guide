from uuid import UUID


class CreateClassFeatureCommand:
    def __init__(
        self, user_id: UUID, class_id: UUID, name: str, description: str, level: int
    ) -> None:
        self.user_id = user_id
        self.class_id = class_id
        self.name = name
        self.description = description
        self.level = level


class UpdateClassFeatureCommand:
    def __init__(
        self,
        user_id: UUID,
        feature_id: UUID,
        class_id: UUID | None,
        name: str | None,
        description: str | None,
        level: int | None,
    ) -> None:
        self.user_id = user_id
        self.feature_id = feature_id
        self.class_id = class_id
        self.name = name
        self.description = description
        self.level = level


class DeleteClassFeatureCommand:
    def __init__(self, user_id: UUID, feature_id: UUID) -> None:
        self.user_id = user_id
        self.feature_id = feature_id

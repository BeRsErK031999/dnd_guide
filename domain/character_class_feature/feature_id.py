from uuid import UUID


class ClassFeatureID:
    def __init__(self, feature_id: UUID) -> None:
        self.__feature_id = feature_id

    def feature_id(self) -> UUID:
        return self.__feature_id

    def __str__(self) -> str:
        return self.__feature_id.__str__()

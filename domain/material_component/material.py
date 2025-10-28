from uuid import UUID

from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName


class MaterialComponent(EntityName, EntityDescription):
    def __init__(
        self,
        material_id: UUID,
        name: str,
        description: str,
    ) -> None:
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self.__material_id = material_id

    def material_id(self) -> UUID:
        return self.__material_id

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__material_id == value.__material_id
        if isinstance(value, UUID):
            return self.__material_id == value
        raise NotImplemented

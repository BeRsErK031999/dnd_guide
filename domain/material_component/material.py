from uuid import UUID

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
        self._material_id = material_id

    def material_id(self) -> UUID:
        return self._material_id

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._material_id == value._material_id
        if isinstance(value, UUID):
            return self._material_id == value
        raise NotImplemented

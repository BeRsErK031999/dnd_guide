from uuid import UUID

from domain.mixin import EntityDescription, EntityName, EntityNameInEnglish


class Source(EntityName, EntityNameInEnglish, EntityDescription):
    def __init__(
        self,
        source_id: UUID,
        name: str,
        description: str,
        name_in_english: str,
    ) -> None:
        EntityName.__init__(self, name)
        EntityNameInEnglish.__init__(self, name_in_english)
        EntityDescription.__init__(self, description)
        self.__source_id = source_id

    def source_id(self) -> UUID:
        return self.__source_id

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__source_id == value.__source_id
        if isinstance(value, UUID):
            return self.__source_id == value
        raise NotImplemented

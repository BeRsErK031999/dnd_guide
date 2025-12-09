from dataclasses import dataclass
from uuid import UUID

from domain.character_subclass import CharacterSubclass

__all__ = ["AppSubclass"]


@dataclass
class AppSubclass:
    subclass_id: UUID
    class_id: UUID
    name: str
    description: str
    name_in_english: str

    @staticmethod
    def from_domain(subclass: CharacterSubclass) -> "AppSubclass":
        return AppSubclass(
            subclass_id=subclass.subclass_id(),
            class_id=subclass.class_id(),
            name=subclass.name(),
            description=subclass.description(),
            name_in_english=subclass.name_in_english(),
        )

    def to_domain(self) -> CharacterSubclass:
        return CharacterSubclass(
            subclass_id=self.subclass_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )

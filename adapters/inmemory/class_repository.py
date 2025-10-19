from uuid import UUID, uuid4

from app_error import AppError
from application.command.character_class import (
    ClassRepository as CommandClassRepository,
)
from domain.character_class import CharacterClass, ClassID, ClassName


class InMemoryClassRepository(CommandClassRepository):
    def __init__(self) -> None:
        self.__class_store: dict[UUID, CharacterClass] = dict()

    def next_class_id(self) -> ClassID:
        return ClassID(uuid4())

    def is_class_of_id_exist(self, class_id: ClassID) -> bool:
        return bool(self.__class_store.get(class_id.class_id(), False))

    def is_class_of_name_exist(self, class_name: ClassName) -> bool:
        for _, character_class in self.__class_store.items():
            if character_class.name() == class_name:
                return True
        return False

    def get_class_of_id(self, class_id: ClassID) -> CharacterClass:
        character_class = self.__class_store.get(class_id.class_id(), None)
        if character_class is None:
            raise AppError.internal(f"класса с id {class_id.class_id()} не существует")
        return character_class

    def class_create(self, character_class: CharacterClass) -> None:
        if self.is_class_of_id_exist(character_class.class_id()):
            raise AppError.internal(
                f"класса с id {character_class.class_id()} уже существует"
            )
        self.__class_store[character_class.class_id().class_id()] = character_class

    def class_update(self, character_class: CharacterClass) -> None:
        if not self.is_class_of_id_exist(character_class.class_id()):
            raise AppError.internal(
                f"класса с id {character_class.class_id()} не существует"
            )
        self.__class_store[character_class.class_id().class_id()] = character_class

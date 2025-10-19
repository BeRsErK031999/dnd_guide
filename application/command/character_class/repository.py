from abc import ABC, abstractmethod

from domain.character_class import CharacterClass, ClassID, ClassName


class ClassRepository(ABC):
    @abstractmethod
    def next_id(self) -> ClassID:
        raise NotImplementedError()

    @abstractmethod
    def is_class_of_id_exist(self, class_id: ClassID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_class_of_name_exist(self, class_name: ClassName) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_class_of_id(self, class_id: ClassID) -> CharacterClass:
        raise NotImplementedError()

    @abstractmethod
    def class_create(self, character_class: CharacterClass) -> None:
        raise NotImplementedError()

    @abstractmethod
    def class_update(self, character_class: CharacterClass) -> None:
        raise NotImplementedError()

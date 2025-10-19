from uuid import UUID

from application.command.character_class.base_command import BaseCommand
from domain.character_class import CharacterClass, ClassDescription, ClassName
from domain.error import DomainError
from domain.user import UserID


class NewClassCommand(BaseCommand):
    def execute(self, row_user_id: UUID, row_name: str, row_description: str) -> None:
        self.assert_access(UserID(row_user_id))
        class_name = ClassName.from_str(row_name)
        if self.__class_repository.is_class_of_name_exist(class_name):
            raise DomainError.idempotent(f"класс {class_name} уже существует")
        character_class = CharacterClass(
            self.__class_repository.next_id(),
            name=class_name,
            description=ClassDescription(row_description),
        )
        self.__class_repository.class_create(character_class)

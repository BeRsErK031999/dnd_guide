from uuid import UUID

from app_error import AppError
from application.command.character_class.base_command import BaseCommand
from domain.character_class import ClassDescription, ClassID
from domain.user import UserID


class NewDescriptionForClassCommand(BaseCommand):
    def execute(
        self, row_user_id: UUID, row_class_id: UUID, row_description: str
    ) -> None:
        self.assert_access(UserID(row_user_id))
        class_id = ClassID(row_class_id)
        description = ClassDescription(row_description)
        if not self.__class_repository.is_class_of_id_exist(class_id):
            raise AppError.not_found(f"класс с ID {class_id} не существует")
        character_class = self.__class_repository.get_class_of_id(class_id)
        character_class.new_description(description)
        self.__class_repository.class_update(character_class)

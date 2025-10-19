from abc import ABC

from application.command.class_feature.repository import ClassFeatureRepository
from application.command.user import UserRepository
from domain.error import AppError
from domain.user.user_id import UserID


class BaseCommand(ABC):
    def __init__(
        self,
        user_repository: UserRepository,
        feature_repository: ClassFeatureRepository,
    ) -> None:
        self.__user_repository = user_repository
        self.__feature_repository = feature_repository

    def assert_access(self, user_id: UserID) -> None:
        if not self.__user_repository.is_user_of_id_exist(user_id):
            raise AppError.access("")

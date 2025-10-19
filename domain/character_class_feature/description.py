from app_error import AppError


class ClassFeatureDescription:
    def __init__(self, description: str) -> None:
        if len(description) == 0:
            raise AppError.invalid_data("у умения не может быть пустое описание")
        self.__description = description

    def description(self) -> str:
        return self.__description

    def __str__(self) -> str:
        return self.__description

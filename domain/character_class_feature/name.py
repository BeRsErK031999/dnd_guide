from domain.error import AppError


class ClassFeatureName:
    def __init__(self, name: str) -> None:
        if len(name) == 0:
            raise AppError.invalid_data("название умения не может быть пустым")
        self.__name = name

    def name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return self.__name

from app_error import AppError


class ClassFeatureLevel:
    def __init__(self, level: int) -> None:
        if level < 1 | level > 20:
            raise AppError.invalid_data(
                "уровень умения должен находиться в диапазоне от 1 до 20"
            )
        self.__level = level

    def level(self) -> int:
        return self.__level

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__level == value.__level
        if isinstance(value, int):
            return self.__level == value
        raise TypeError(
            f"класс {self.__class__.__name__} невозможно сравнить с {value.__class__.__name__}"
        )

    def __lt__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__level < value.__level
        if isinstance(value, int):
            return self.__level < value
        raise TypeError(
            f"класс {self.__class__.__name__} невозможно сравнить с {value.__class__.__name__}"
        )

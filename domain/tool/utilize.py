from domain.error import DomainError


class ToolUtilize:
    def __init__(self, action: str, complexity: int) -> None:
        if len(action) == 0:
            raise DomainError.invalid_data("название действия не может быть пустым")
        if complexity < 0 or complexity > 20:
            raise DomainError.invalid_data(
                "сложность действия должна находиться в диапазоне от 0 до 20"
            )
        self._action = action
        self._complexity = complexity

    def action(self) -> str:
        return self._action

    def complexity(self) -> int:
        return self._complexity

    def __str__(self) -> str:
        return f"{self._action} (сложность {self._complexity})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._action == value._action and self._complexity == value._complexity
            )
        raise NotImplemented

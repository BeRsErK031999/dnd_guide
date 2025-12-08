from domain.error import DomainError
from domain.mixin import ValueDescription, ValueName


class SubraceFeature(ValueName, ValueDescription):
    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        ValueName.__init__(self, name)
        ValueDescription.__init__(self, description)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._name == value._name and self._description == value._description
        raise NotImplemented

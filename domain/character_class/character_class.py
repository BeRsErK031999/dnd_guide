from domain.character_class.class_id import ClassID
from domain.character_class.description import ClassDescription
from domain.character_class.name import ClassName
from domain.dice import Dice


class CharacterClass:
    def __init__(
        self,
        class_id: ClassID,
        name: ClassName,
        description: ClassDescription,
    ) -> None:
        self.__class_id = class_id
        self.__name = name
        self.__description = description

    def __init_bard(self) -> None:
        pass

    def __init_barbarian(self) -> None:
        pass

    def __init_fighter(self) -> None:
        pass

    def __init_wizard(self) -> None:
        pass

    def __init_druid(self) -> None:
        pass

    def __init_cleric(self) -> None:
        pass

    def __init_warlock(self) -> None:
        pass

    def __init_monk(self) -> None:
        pass

    def __init_paladin(self) -> None:
        pass

    def __init_rogue(self) -> None:
        pass

    def __init_ranger(self) -> None:
        pass

    def __init_sorcerer(self) -> None:
        pass

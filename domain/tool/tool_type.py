from enum import StrEnum

from domain.error import DomainError


class ToolType(StrEnum):
    ARTISANS_TOOLS = "ремесленные инструменты"
    GAMING_SETS = "игровые наборы"
    MUSICAL_INSTRUMENTS = "музыкальные инструменты"
    THIEVES_TOOLS = "воровские инструменты"
    DISGUISE_KIT = "набор для маскировки"
    FORGERY_KIT = "набор для фальсификации"
    HERBALISM_KIT = "набор травника"
    NAVIGATORS_TOOLS = "инструменты навигатора"
    POISONERS_KIT = "набор отравителя"

    @staticmethod
    def from_str(name: str) -> ToolType:
        match name.upper():
            case ToolType.ARTISANS_TOOLS.name:
                return ToolType.ARTISANS_TOOLS
            case ToolType.GAMING_SETS.name:
                return ToolType.GAMING_SETS
            case ToolType.MUSICAL_INSTRUMENTS.name:
                return ToolType.MUSICAL_INSTRUMENTS
            case ToolType.THIEVES_TOOLS.name:
                return ToolType.THIEVES_TOOLS
            case ToolType.DISGUISE_KIT.name:
                return ToolType.DISGUISE_KIT
            case ToolType.FORGERY_KIT.name:
                return ToolType.FORGERY_KIT
            case ToolType.HERBALISM_KIT.name:
                return ToolType.HERBALISM_KIT
            case ToolType.NAVIGATORS_TOOLS.name:
                return ToolType.NAVIGATORS_TOOLS
            case ToolType.POISONERS_KIT.name:
                return ToolType.POISONERS_KIT
            case _:
                raise DomainError.invalid_data(
                    f"для типа инструмента с названием {name} не удалось сопоставить значение"
                )

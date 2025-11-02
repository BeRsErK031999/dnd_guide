from typing import Sequence
from uuid import UUID

from domain.error import DomainError


class CharacterClassCreateCommand:
    def __init__(
        self,
        user_id: UUID,
        name: str,
        description: str,
        primary_modifiers: Sequence[str],
        hit_dice: str,
        starting_hits: int,
        hit_modifier: str,
        next_level_hits: int,
        armors: Sequence[str],
        weapon: Sequence[UUID],
        tools: Sequence[UUID],
        saving_throws: Sequence[str],
        skills: Sequence[str],
        number_skills: int,
        number_tools: int = 1,
        name_in_english: str = "",
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.description = description
        self.primary_modifiers = primary_modifiers
        self.hit_dice = hit_dice
        self.starting_hits = starting_hits
        self.hit_modifier = hit_modifier
        self.next_level_hits = next_level_hits
        self.armors = armors
        self.weapon = weapon
        self.tools = tools
        self.saving_throws = saving_throws
        self.skills = skills
        self.number_skills = number_skills
        self.number_tools = number_tools
        self.name_in_english = name_in_english


class CharacterClassUpdateCommand:
    def __init__(
        self,
        user_id: UUID,
        class_id: UUID,
        name: str | None,
        description: str | None,
        primary_modifiers: Sequence[str] | None,
        hit_dice: str | None,
        starting_hits: int | None,
        hit_modifier: str | None,
        next_level_hits: int | None,
        armors: Sequence[str] | None,
        weapon: Sequence[UUID] | None,
        tools: Sequence[UUID] | None,
        saving_throws: Sequence[str] | None,
        skills: Sequence[str] | None,
        number_skills: int | None,
        number_tools: int | None,
        name_in_english: str | None = None,
    ) -> None:
        if all(
            [
                name is None,
                description is None,
                primary_modifiers is None,
                hit_dice is None,
                starting_hits is None,
                hit_modifier is None,
                next_level_hits is None,
                armors is None,
                weapon is None,
                tools is None,
                saving_throws is None,
                skills is None,
                number_skills is None,
                number_tools is None,
                name_in_english is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления класса")
        if any(
            [
                hit_dice is not None,
                starting_hits is not None,
                hit_modifier is not None,
                next_level_hits is not None,
            ]
        ) and not all(
            [
                hit_dice is not None,
                starting_hits is not None,
                hit_modifier is not None,
                next_level_hits is not None,
            ]
        ):
            raise DomainError.invalid_data(
                "для обновления хитов здоровья не все данные переданы"
            )
        if any(
            [
                armors is not None,
                weapon is not None,
                tools is not None,
                saving_throws is not None,
                skills is not None,
                number_skills is not None,
                number_tools is not None,
            ]
        ) and not all(
            [
                armors is not None,
                weapon is not None,
                tools is not None,
                saving_throws is not None,
                skills is not None,
                number_skills is not None,
                number_tools is not None,
            ]
        ):
            raise DomainError.invalid_data(
                "для обновления владений не все данные переданы"
            )
        self.user_id = user_id
        self.class_id = class_id
        self.name = name
        self.description = description
        self.primary_modifiers = primary_modifiers
        self.hit_dice = hit_dice
        self.starting_hits = starting_hits
        self.hit_modifier = hit_modifier
        self.next_level_hits = next_level_hits
        self.armors = armors
        self.weapon = weapon
        self.tools = tools
        self.saving_throws = saving_throws
        self.skills = skills
        self.number_skills = number_skills
        self.number_tools = number_tools
        self.name_in_english = name_in_english


class CharacterClassDeleteCommand:
    def __init__(self, user_id: UUID, class_id: UUID) -> None:
        self.user_id = user_id
        self.class_id = class_id

from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.class_level import (
    ClassLevel,
    ClassLevelBonusDamage,
    ClassLevelDice,
    ClassLevelIncreaseSpeed,
    ClassLevelPoints,
    ClassLevelSpellSlots,
)
from domain.dice import Dice, DiceType
from domain.length import Length, LengthUnit
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel


class ClassLevelModel(Base):
    __tablename__ = "class_level"

    level: Mapped[int]
    dice_name: Mapped[str | None]
    dice_count: Mapped[int | None]
    dice_description: Mapped[str | None]
    number_cantrips_know: Mapped[int | None]
    number_spells_know: Mapped[int | None]
    number_arcanums_know: Mapped[int | None]
    points: Mapped[int | None]
    points_description: Mapped[str | None]
    bonus_damage: Mapped[int | None]
    bonus_damage_description: Mapped[str | None]
    increase_speed: Mapped[float | None]
    increase_speed_description: Mapped[str | None]
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="class_levels"
    )
    class_level_spell_slot: Mapped["ClassLevelSpellSlotModel | None"] = relationship(
        back_populates="class_level"
    )

    def to_domain(self) -> ClassLevel:
        dice = None
        spell_slots = None
        points = None
        bonus_damage = None
        increase_speed = None
        if (
            self.dice_count is not None
            and self.dice_name is not None
            and self.dice_description is not None
        ):
            dice = ClassLevelDice(
                dice=Dice(
                    count=self.dice_count, dice_type=DiceType.from_str(self.dice_name)
                ),
                dice_description=self.dice_description,
            )
        if self.class_level_spell_slot is not None:
            spell_slots = self.class_level_spell_slot.to_domain()
        if self.points is not None and self.points_description is not None:
            points = ClassLevelPoints(
                points=self.points, description=self.points_description
            )
        if self.bonus_damage is not None and self.bonus_damage_description is not None:
            bonus_damage = ClassLevelBonusDamage(
                damage=self.bonus_damage,
                description=self.bonus_damage_description,
            )
        if (
            self.increase_speed is not None
            and self.increase_speed_description is not None
        ):
            increase_speed = ClassLevelIncreaseSpeed(
                speed=Length(count=self.increase_speed, unit=LengthUnit.FT),
                description=self.increase_speed_description,
            )
        return ClassLevel(
            level_id=self.id,
            class_id=self.character_class_id,
            level=self.level,
            dice=dice,
            spell_slots=spell_slots,
            number_cantrips_know=self.number_cantrips_know,
            number_spells_know=self.number_spells_know,
            number_arcanums_know=self.number_arcanums_know,
            points=points,
            bonus_damage=bonus_damage,
            increase_speed=increase_speed,
        )

    @staticmethod
    def from_domain(class_level: ClassLevel) -> "ClassLevelModel":
        dice = class_level.dice()
        points = class_level.points()
        bonus_damage = class_level.bonus_damage()
        increase_speed = class_level.increase_speed()
        return ClassLevelModel(
            id=class_level.level_id(),
            level=class_level.level(),
            dice_name=dice.dice().dice_type().name if dice is not None else None,
            dice_count=dice.dice().count() if dice is not None else None,
            dice_description=dice.description() if dice is not None else None,
            number_cantrips_know=class_level.number_cantrips_know(),
            number_spells_know=class_level.number_spells_know(),
            number_arcanums_know=class_level.number_arcanums_know(),
            points=points.points() if points is not None else None,
            points_description=points.description() if points is not None else None,
            bonus_damage=bonus_damage.damage() if bonus_damage is not None else None,
            bonus_damage_description=(
                bonus_damage.description() if bonus_damage is not None else None
            ),
            increase_speed=(
                increase_speed.speed().in_ft() if increase_speed is not None else None
            ),
            increase_speed_description=(
                increase_speed.description() if increase_speed is not None else None
            ),
            character_class_id=class_level.class_id(),
        )


class ClassLevelSpellSlotModel(Base):
    __tablename__ = "class_level_spell_slot"

    level_1: Mapped[int]
    level_2: Mapped[int]
    level_3: Mapped[int]
    level_4: Mapped[int]
    level_5: Mapped[int]
    level_6: Mapped[int]
    level_7: Mapped[int]
    level_8: Mapped[int]
    level_9: Mapped[int]
    class_level_id: Mapped[UUID] = mapped_column(ForeignKey("class_level.id"))

    class_level: Mapped["ClassLevelModel"] = relationship(
        back_populates="class_level_spell_slot"
    )

    def to_domain(self) -> ClassLevelSpellSlots:
        return ClassLevelSpellSlots(
            spell_slots=[
                self.level_1,
                self.level_2,
                self.level_3,
                self.level_4,
                self.level_5,
                self.level_6,
                self.level_7,
                self.level_8,
                self.level_9,
            ]
        )

    @staticmethod
    def from_domain(
        class_level_id: UUID, spell_slots: ClassLevelSpellSlots
    ) -> "ClassLevelSpellSlotModel":
        slots = spell_slots.slots()
        return ClassLevelSpellSlotModel(
            level_1=slots[0],
            level_2=slots[1],
            level_3=slots[2],
            level_4=slots[3],
            level_5=slots[4],
            level_6=slots[5],
            level_7=slots[6],
            level_8=slots[7],
            level_9=slots[8],
            class_level_id=class_level_id,
        )

from typing import TYPE_CHECKING, Sequence
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.coin import Coins, PieceType
from domain.damage_type import DamageType
from domain.dice import Dice, DiceType
from domain.length import Length, LengthUnit
from domain.weapon import Weapon, WeaponDamage
from domain.weapon_kind import WeaponKind, WeaponType
from domain.weapon_property import WeaponProperty, WeaponPropertyName
from domain.weight import Weight, WeightUnit
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel
    from adapters.repository.sql.models.material import MaterialModel


class WeaponModel(Base):
    __tablename__ = "weapon"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    cost: Mapped[int]
    damage_dice_name: Mapped[str]
    damage_dice_count: Mapped[int]
    damage_type: Mapped[str]
    bonus_damage: Mapped[int]
    weight: Mapped[float]
    material_id: Mapped[UUID] = mapped_column(ForeignKey("material.id"))
    kind_id: Mapped[UUID] = mapped_column(ForeignKey("weapon_kind.id"))

    material: Mapped[MaterialModel] = relationship(back_populates="weapons")
    kind: Mapped[WeaponKindModel] = relationship(back_populates="weapons")
    properties: Mapped[list[WeaponPropertyModel]] = relationship(
        back_populates="weapons", secondary="rel_weapon_property"
    )
    character_classes: Mapped[list[CharacterClassModel]] = relationship(
        back_populates="weapons", secondary="rel_class_weapon"
    )

    def to_domain(self) -> Weapon:
        return Weapon(
            weapon_id=self.id,
            weapon_kind_id=self.kind_id,
            name=self.name,
            description=self.description,
            cost=Coins(count=self.cost, piece_type=PieceType.COPPER),
            damage=WeaponDamage(
                dice=Dice(
                    count=self.damage_dice_count,
                    dice_type=DiceType.from_str(self.damage_dice_name),
                ),
                damage_type=DamageType.from_str(self.damage_type),
                bonus_damage=self.bonus_damage,
            ),
            weight=Weight(count=self.weight, unit=WeightUnit.LB),
            weapon_property_ids=[p.id for p in self.properties],
            material_id=self.material_id,
        )

    @staticmethod
    def from_domain(weapon: Weapon) -> WeaponModel:
        return WeaponModel(
            id=weapon.weapon_id(),
            name=weapon.name(),
            description=weapon.description(),
            cost=weapon.cost().in_copper(),
            damage_dice_name=weapon.damage().dice().dice_type().name,
            damage_dice_count=weapon.damage().dice().count(),
            damage_type=weapon.damage().damage_type().name,
            bonus_damage=weapon.damage().bonus_damage(),
            weight=weapon.weight().in_lb(),
            kind_id=weapon.kind_id(),
            material_id=weapon.material_id(),
        )


class WeaponPropertyModel(Base):
    __tablename__ = "weapon_property"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    base_range: Mapped[float | None]
    max_range: Mapped[float | None]
    second_hand_dice_name: Mapped[str | None]
    second_hand_dice_count: Mapped[int | None]

    weapons: Mapped[list[WeaponModel]] = relationship(
        back_populates="properties", secondary="rel_weapon_property"
    )

    def to_domain(self) -> WeaponProperty:
        return WeaponProperty(
            weapon_property_id=self.id,
            name=WeaponPropertyName.from_str(self.name),
            description=self.description,
            base_range=(
                Length(count=self.base_range, unit=LengthUnit.FT)
                if not self.base_range is None
                else None
            ),
            max_range=(
                Length(count=self.max_range, unit=LengthUnit.FT)
                if not self.max_range is None
                else None
            ),
            second_hand_dice=(
                Dice(
                    count=self.second_hand_dice_count,
                    dice_type=DiceType.from_str(self.second_hand_dice_name),
                )
                if self.second_hand_dice_count is not None
                and self.second_hand_dice_name is not None
                else None
            ),
        )

    @staticmethod
    def from_domain(
        weapon_property: WeaponProperty,
    ) -> WeaponPropertyModel:
        base_range = weapon_property.base_range()
        max_range = weapon_property.max_range()
        dice = weapon_property.second_hand_dice()
        return WeaponPropertyModel(
            id=weapon_property.weapon_property_id(),
            name=weapon_property.name().name,
            description=weapon_property.description(),
            base_range=base_range.in_ft() if base_range else None,
            max_range=(max_range.in_ft() if max_range else None),
            second_hand_dice_name=(dice.dice_type().name if dice is not None else None),
            second_hand_dace_count=(dice.count() if dice is not None else None),
        )


class WeaponKindModel(Base):
    __tablename__ = "weapon_kind"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    weapon_type: Mapped[str] = mapped_column(String(50))

    weapons: Mapped[list[WeaponModel]] = relationship(back_populates="kind")

    def to_domain(self) -> WeaponKind:
        return WeaponKind(
            weapon_kind_id=self.id,
            name=self.name,
            description=self.description,
            weapon_type=WeaponType.from_str(self.weapon_type),
        )

    @staticmethod
    def from_domain(weapon_kind: WeaponKind) -> WeaponKindModel:
        return WeaponKindModel(
            id=weapon_kind.weapon_kind_id(),
            name=weapon_kind.name(),
            description=weapon_kind.description(),
            weapon_type=weapon_kind.weapon_type().name,
        )


class RelWeaponPropertyModel(Base):
    __tablename__ = "rel_weapon_property"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"), unique=True)
    weapon_property_id: Mapped[UUID] = mapped_column(ForeignKey("weapon_property.id"))

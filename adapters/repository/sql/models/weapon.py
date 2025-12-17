from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.coin import AppCoins
from application.dto.model.dice import AppDice
from application.dto.model.length import AppLength
from application.dto.model.weapon import AppWeapon, AppWeaponDamage
from application.dto.model.weapon_kind import AppWeaponKind
from application.dto.model.weapon_property import AppWeaponProperty
from application.dto.model.weight import AppWeight
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

    material: Mapped["MaterialModel"] = relationship(back_populates="weapons")
    kind: Mapped["WeaponKindModel"] = relationship(back_populates="weapons")
    properties: Mapped[list["WeaponPropertyModel"]] = relationship(
        back_populates="weapons", secondary="rel_weapon_property"
    )
    character_classes: Mapped[list["CharacterClassModel"]] = relationship(
        back_populates="weapons", secondary="rel_class_weapon"
    )

    def to_app(self) -> AppWeapon:
        return AppWeapon(
            weapon_id=self.id,
            weapon_kind_id=self.kind_id,
            name=self.name,
            description=self.description,
            cost=AppCoins(count=self.cost),
            damage=AppWeaponDamage(
                dice=AppDice(
                    count=self.damage_dice_count, dice_type=self.damage_dice_name
                ),
                damage_type=self.damage_type,
                bonus_damage=self.bonus_damage,
            ),
            weight=AppWeight(count=self.weight),
            weapon_property_ids=[p.id for p in self.properties],
            material_id=self.material_id,
        )

    @staticmethod
    def from_app(weapon: AppWeapon) -> "WeaponModel":
        return WeaponModel(
            id=weapon.weapon_id,
            name=weapon.name,
            description=weapon.description,
            cost=weapon.cost.count,
            damage_dice_name=weapon.damage.dice.dice_type,
            damage_dice_count=weapon.damage.dice.count,
            damage_type=weapon.damage.damage_type,
            bonus_damage=weapon.damage.bonus_damage,
            weight=weapon.weight.count,
            kind_id=weapon.weapon_kind_id,
            material_id=weapon.material_id,
        )


class WeaponPropertyModel(Base):
    __tablename__ = "weapon_property"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    base_range: Mapped[float | None]
    max_range: Mapped[float | None]
    second_hand_dice_name: Mapped[str | None]
    second_hand_dice_count: Mapped[int | None]

    weapons: Mapped[list["WeaponModel"]] = relationship(
        back_populates="properties", secondary="rel_weapon_property"
    )

    def to_app(self) -> AppWeaponProperty:
        return AppWeaponProperty(
            weapon_property_id=self.id,
            name=self.name,
            description=self.description,
            base_range=(
                AppLength(count=self.base_range)
                if not self.base_range is None
                else None
            ),
            max_range=(
                AppLength(count=self.max_range) if not self.max_range is None else None
            ),
            second_hand_dice=(
                AppDice(
                    count=self.second_hand_dice_count,
                    dice_type=self.second_hand_dice_name,
                )
                if self.second_hand_dice_count is not None
                and self.second_hand_dice_name is not None
                else None
            ),
        )

    @staticmethod
    def from_app(
        weapon_property: AppWeaponProperty,
    ) -> "WeaponPropertyModel":
        base_range = weapon_property.base_range
        max_range = weapon_property.max_range
        dice = weapon_property.second_hand_dice
        return WeaponPropertyModel(
            id=weapon_property.weapon_property_id,
            name=weapon_property.name,
            description=weapon_property.description,
            base_range=base_range.count if base_range else None,
            max_range=max_range.count if max_range else None,
            second_hand_dice_name=dice.dice_type if dice is not None else None,
            second_hand_dice_count=dice.count if dice is not None else None,
        )


class WeaponKindModel(Base):
    __tablename__ = "weapon_kind"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    weapon_type: Mapped[str] = mapped_column(String(50))

    weapons: Mapped[list["WeaponModel"]] = relationship(back_populates="kind")

    def to_app(self) -> AppWeaponKind:
        return AppWeaponKind(
            weapon_kind_id=self.id,
            name=self.name,
            description=self.description,
            weapon_type=self.weapon_type,
        )

    @staticmethod
    def from_app(weapon_kind: AppWeaponKind) -> "WeaponKindModel":
        return WeaponKindModel(
            id=weapon_kind.weapon_kind_id,
            name=weapon_kind.name,
            description=weapon_kind.description,
            weapon_type=weapon_kind.weapon_type,
        )


class RelWeaponPropertyModel(Base):
    __tablename__ = "rel_weapon_property"

    weapon_id: Mapped[UUID] = mapped_column(
        ForeignKey("weapon.id", ondelete="CASCADE"), unique=True
    )
    weapon_property_id: Mapped[UUID] = mapped_column(
        ForeignKey("weapon_property.id", ondelete="CASCADE")
    )

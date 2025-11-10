from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.postgres.models.base import Base
from adapters.repository.postgres.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.postgres.models.character_class import CharacterClass


class Weapon(Timestamp, Base):
    __tablename__ = "weapon"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    cost: Mapped[int]
    damage_dice_name: Mapped[str]
    damage_dice_count: Mapped[int]
    damage_type: Mapped[str]
    bonus_damage: Mapped[int]
    weight: Mapped[float]
    properties: Mapped[list["WeaponProperty"]] = relationship(
        back_populates="weapons", secondary="rel_weapon_property"
    )
    kind: Mapped[list["WeaponKind"]] = relationship(
        back_populates="weapons", secondary="rel_weapon_kind"
    )
    character_classes: Mapped[list["CharacterClass"]] = relationship(
        back_populates="weapons", secondary="rel_class_weapon"
    )


class WeaponProperty(Timestamp, Base):
    __tablename__ = "weapon_property"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    base_range: Mapped[int | None]
    max_range: Mapped[int | None]
    second_hand_dice_name: Mapped[str | None]
    second_hand_dace_count: Mapped[int | None]
    weapons: Mapped[list["Weapon"]] = relationship(
        "Weapon", secondary="rel_weapon_property"
    )
    weapons: Mapped[list["Weapon"]] = relationship(
        back_populates="properties", secondary="rel_weapon_property"
    )


class WeaponKind(Timestamp, Base):
    __tablename__ = "weapon_kind"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    weapon_type: Mapped[str] = mapped_column(String(100))
    weapons: Mapped[list["Weapon"]] = relationship(
        back_populates="kind", secondary="rel_weapon_kind"
    )


class RelWeaponProperty(Timestamp, Base):
    __tablename__ = "rel_weapon_property"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"), unique=True)
    weapon_property_id: Mapped[UUID] = mapped_column(ForeignKey("weapon_property.id"))


class RelWeaponKind(Timestamp, Base):
    __tablename__ = "rel_weapon_kind"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"))
    weapon_kind_id: Mapped[UUID] = mapped_column(ForeignKey("weapon_kind.id"))

from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import WeaponKindModel
from application.repository import WeaponKindRepository as AppWeaponKindRepository
from domain.weapon_kind import WeaponKind
from domain.weapon_kind import WeaponKindRepository as DomainWeaponKindRepository
from sqlalchemy import delete, exists, select


class InMemoryWeaponKindRepository(DomainWeaponKindRepository, AppWeaponKindRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponKindModel)).where(WeaponKindModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, weapon_kind_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(WeaponKindModel)).where(
                WeaponKindModel.id == weapon_kind_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, weapon_kind_id: UUID) -> WeaponKind:
        async with self.__helper.session as session:
            query = select(WeaponKindModel).where(WeaponKindModel.id == weapon_kind_id)
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain_weapon_kind()

    async def get_all(self) -> list[WeaponKind]:
        async with self.__helper.session as session:
            query = select(WeaponKindModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain_weapon_kind() for item in result]

    async def create(self, weapon_kind: WeaponKind) -> None:
        async with self.__helper.session as session:
            session.add(WeaponKindModel.from_domain_weapon_kind(weapon_kind))
            await session.commit()

    async def update(self, weapon_kind: WeaponKind) -> None:
        async with self.__helper.session as session:
            query = select(WeaponKindModel).where(
                WeaponKindModel.id == weapon_kind.weapon_kind_id
            )
            model = await session.execute(query)
            model = model.scalar_one()
            old_domain = model.to_domain_weapon_kind()
            if old_domain.name() != weapon_kind.name():
                model.name = weapon_kind.name()
            if old_domain.description() != weapon_kind.description():
                model.description = weapon_kind.description()
            if old_domain.weapon_type() != weapon_kind.weapon_type():
                model.weapon_type = weapon_kind.weapon_type().name
            await session.commit()

    async def delete(self, weapon_kind_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(WeaponKindModel).where(WeaponKindModel.id == weapon_kind_id)
            await session.execute(stmt)
            await session.commit()

from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import MaterialComponentModel
from application.dto.model.material_component import AppMaterialComponent
from application.repository import (
    MaterialComponentRepository as AppMaterialComponentRepository,
)
from domain.error import DomainError
from domain.material_component import (
    MaterialComponentRepository as DomainMaterialComponentRepository,
)
from sqlalchemy import delete, exists, select


class SQLMaterialComponentRepository(
    DomainMaterialComponentRepository, AppMaterialComponentRepository
):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__db_helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(MaterialComponentModel)).where(
                MaterialComponentModel.name == name
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, material_id: UUID) -> bool:
        async with self.__db_helper.session as session:
            query = select(exists(MaterialComponentModel)).where(
                MaterialComponentModel.id == material_id
            )
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, material_id: UUID) -> AppMaterialComponent:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel).where(
                MaterialComponentModel.id == material_id
            )
            result = await session.execute(query)
            result = result.scalar()
            if result is None:
                raise DomainError.not_found(
                    f"материала с id {material_id} не существует"
                )
            return result.to_app()

    async def get_all(self) -> list[AppMaterialComponent]:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_app() for item in result]

    async def filter(
        self, search_by_name: str | None = None
    ) -> list[AppMaterialComponent]:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel)
            if search_by_name is not None:
                query = query.where(
                    MaterialComponentModel.name.ilike(f"%{search_by_name}%")
                )
            result = await session.execute(query)
            return [item.to_app() for item in result.scalars().all()]

    async def save(self, material: AppMaterialComponent) -> None:
        async with self.__db_helper.session as session:
            await session.merge(MaterialComponentModel.from_app(material))
            await session.commit()

    async def delete(self, material_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(MaterialComponentModel).where(
                MaterialComponentModel.id == material_id
            )
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise DomainError.not_found(
                    f"материала с id {material_id} не существует"
                )
            await session.commit()

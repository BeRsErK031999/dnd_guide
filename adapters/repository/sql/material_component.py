from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import MaterialComponentModel
from application.repository import (
    MaterialComponentRepository as AppMaterialComponentRepository,
)
from domain.material_component import MaterialComponent
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

    async def get_by_id(self, material_id: UUID) -> MaterialComponent:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel).where(
                MaterialComponentModel.id == material_id
            )
            result = await session.execute(query)
            result = result.scalar_one()
            return result.to_domain()

    async def get_all(self) -> list[MaterialComponent]:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel)
            result = await session.execute(query)
            result = result.scalars().all()
            return [item.to_domain() for item in result]

    async def filter(
        self, search_by_name: str | None = None
    ) -> list[MaterialComponent]:
        async with self.__db_helper.session as session:
            query = select(MaterialComponentModel)
            if search_by_name is not None:
                query = query.where(
                    MaterialComponentModel.name.ilike(f"%{search_by_name}%")
                )
            result = await session.execute(query)
            return [item.to_domain() for item in result.scalars().all()]

    async def create(self, material: MaterialComponent) -> None:
        async with self.__db_helper.session as session:
            material_model = MaterialComponentModel.from_domain(material)
            session.add(material_model)
            await session.commit()

    async def update(self, material: MaterialComponent) -> None:
        async with self.__db_helper.session as session:
            await session.merge(MaterialComponentModel.from_domain(material))
            await session.commit()

    async def delete(self, material_id: UUID) -> None:
        async with self.__db_helper.session as session:
            stmt = delete(MaterialComponentModel).where(
                MaterialComponentModel.id == material_id
            )
            await session.execute(stmt)
            await session.commit()

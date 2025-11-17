from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models.material import MaterialModel
from application.repository import MaterialRepository as AppMaterialRepository
from domain.material import Material
from domain.material import MaterialRepository as DomainMaterialRepository
from sqlalchemy import delete, exists, select


class SQLMaterialRepository(DomainMaterialRepository, AppMaterialRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(MaterialModel)).where(MaterialModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, material_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(MaterialModel)).where(MaterialModel.id == material_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, material_id: UUID) -> Material:
        async with self.__helper.session as session:
            query = select(MaterialModel).where(MaterialModel.id == material_id)
            result = await session.execute(query)
            material_model = result.scalar_one()
            return material_model.to_domain()

    async def get_all(self) -> list[Material]:
        async with self.__helper.session as session:
            query = select(MaterialModel)
            result = await session.execute(query)
            return [model.to_domain() for model in result.scalars().all()]

    async def filter(self, search_by_name: str) -> list[Material]:
        async with self.__helper.session as session:
            query = select(MaterialModel).where(
                MaterialModel.name.ilike(f"%{search_by_name}%")
            )
            result = await session.execute(query)
            return [model.to_domain() for model in result.scalars().all()]

    async def create(self, material: Material) -> None:
        async with self.__helper.session as session:
            session.add(MaterialModel.from_domain(material))
            await session.commit()

    async def update(self, material: Material) -> None:
        async with self.__helper.session as session:
            await session.merge(MaterialModel.from_domain(material))
            await session.commit()

    async def delete(self, material_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(MaterialModel).where(MaterialModel.id == material_id)
            await session.execute(stmt)
            await session.commit()

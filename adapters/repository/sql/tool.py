from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import ToolModel, ToolUtilizeModel
from application.dto.model.tool import AppTool
from application.repository import ToolRepository as AppToolRepository
from domain.error import DomainError
from domain.tool import ToolRepository as DomainToolRepository
from sqlalchemy import delete, exists, select
from sqlalchemy.orm import selectinload


class SQLToolRepository(DomainToolRepository, AppToolRepository):
    def __init__(self, db_helper: DBHelper) -> None:
        self.__helper = db_helper

    async def name_exists(self, name: str) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ToolModel)).where(ToolModel.name == name)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, tool_id: UUID) -> bool:
        async with self.__helper.session as session:
            query = select(exists(ToolModel)).where(ToolModel.id == tool_id)
            result = await session.execute(query)
            result = result.scalar()
            return result if result is not None else False

    async def get_by_id(self, tool_id: UUID) -> AppTool:
        async with self.__helper.session as session:
            query = (
                select(ToolModel)
                .where(ToolModel.id == tool_id)
                .options(selectinload(ToolModel.utilizes))
            )
            result = await session.execute(query)
            tool_model = result.scalar()
            if tool_model is None:
                raise DomainError.not_found(f"инструмента с id {tool_id} не существует")
            return tool_model.to_app()

    async def get_all(self) -> list[AppTool]:
        async with self.__helper.session as session:
            stmt = select(ToolModel).options(selectinload(ToolModel.utilizes))
            result = await session.execute(stmt)
            return [tool_model.to_app() for tool_model in result.scalars().all()]

    async def filter(self, search_by_name: str | None = None) -> list[AppTool]:
        async with self.__helper.session as session:
            query = select(ToolModel).options(selectinload(ToolModel.utilizes))
            if search_by_name is not None:
                query = query.where(ToolModel.name.ilike(f"%{search_by_name}%"))
            result = await session.execute(query)
            return [tool_model.to_app() for tool_model in result.scalars().all()]

    async def save(self, tool: AppTool) -> None:
        if await self.id_exists(tool.tool_id):
            await self.update(tool)
        else:
            await self.create(tool)

    async def create(self, tool: AppTool) -> None:
        async with self.__helper.session as session:
            model = ToolModel.from_app(tool)
            if len(tool.utilizes) > 0:
                model.utilizes.extend(
                    [
                        ToolUtilizeModel.from_app(tool.tool_id, utilize)
                        for utilize in tool.utilizes
                    ]
                )
            session.add(model)
            await session.commit()

    async def update(self, tool: AppTool) -> None:
        async with self.__helper.session as session:
            query = (
                select(ToolModel)
                .where(ToolModel.id == tool.tool_id)
                .options(selectinload(ToolModel.utilizes))
            )
            result = await session.execute(query)
            model = result.scalar_one()
            old = model.to_app()
            if tool.tool_type != old.tool_type:
                model.tool_type = tool.tool_type
            if tool.name != old.name:
                model.name = tool.name
            if tool.cost != old.cost:
                model.cost = tool.cost.count
            if tool.weight != old.weight:
                model.weight = tool.weight.count
            model.utilizes.clear()
            model.utilizes.extend(
                [
                    ToolUtilizeModel.from_app(tool.tool_id, utilize)
                    for utilize in tool.utilizes
                ]
            )
            model.description = tool.description
            await session.commit()

    async def delete(self, tool_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ToolModel).where(ToolModel.id == tool_id)
            result = await session.execute(stmt)
            if result.rowcount == 0:
                raise DomainError.not_found(f"инструмента с id {tool_id} не существует")
            await session.commit()

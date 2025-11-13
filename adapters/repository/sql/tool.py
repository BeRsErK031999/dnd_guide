from uuid import UUID, uuid4

from adapters.repository.sql.database import DBHelper
from adapters.repository.sql.models import ToolModel, ToolUtilizeModel
from application.repository import ToolRepository as AppToolRepository
from domain.tool import Tool
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

    async def get_by_id(self, tool_id: UUID) -> Tool:
        async with self.__helper.session as session:
            query = (
                select(ToolModel)
                .where(ToolModel.id == tool_id)
                .options(selectinload(ToolModel.utilizes))
            )
            result = await session.execute(query)
            tool_model = result.scalar_one()
            return tool_model.to_domain()

    async def get_all(self) -> list[Tool]:
        async with self.__helper.session as session:
            stmt = select(ToolModel).options(selectinload(ToolModel.utilizes))
            result = await session.execute(stmt)
            return [tool_model.to_domain() for tool_model in result.scalars().all()]

    async def create(self, tool: Tool) -> None:
        async with self.__helper.session as session:
            model = ToolModel.from_domain(tool)
            if len(tool.utilizes()) > 0:
                model.utilizes.extend(
                    [
                        ToolUtilizeModel.from_domain(tool.tool_id(), utilize)
                        for utilize in tool.utilizes()
                    ]
                )
            session.add(model)
            await session.commit()

    async def update(self, tool: Tool) -> None:
        async with self.__helper.session as session:
            query = (
                select(ToolModel)
                .where(ToolModel.id == tool.tool_id())
                .options(selectinload(ToolModel.utilizes))
            )
            result = await session.execute(query)
            model = result.scalar_one()
            old_domain = model.to_domain()
            if tool.tool_type() != old_domain.tool_type():
                model.tool_type = tool.tool_type().name
            if tool.name() != old_domain.name():
                model.name = tool.name()
            if tool.cost() != old_domain.cost():
                model.cost = tool.cost().in_copper()
            if tool.weight() != old_domain.weight():
                model.weight = tool.weight().in_lb()
            model.utilizes.clear()
            model.utilizes.extend(
                [
                    ToolUtilizeModel.from_domain(tool.tool_id(), utilize)
                    for utilize in tool.utilizes()
                ]
            )
            model.description = tool.description()
            await session.commit()

    async def delete(self, tool_id: UUID) -> None:
        async with self.__helper.session as session:
            stmt = delete(ToolModel).where(ToolModel.id == tool_id)
            await session.execute(stmt)
            await session.commit()

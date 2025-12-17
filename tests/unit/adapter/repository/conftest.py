import pytest
import pytest_asyncio
from adapters.repository.sql import DBHelper
from adapters.repository.sql.models import Base


@pytest_asyncio.fixture(scope="session")
async def create_db_helper():
    helper = DBHelper(db_url="sqlite+aiosqlite:///:memory:")
    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield helper
    await helper.engine.dispose()


@pytest_asyncio.fixture
async def db_helper(create_db_helper):
    async with create_db_helper.engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
    yield create_db_helper

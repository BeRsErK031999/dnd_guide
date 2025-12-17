from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.subrace import AppSubrace


class SubraceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, subrace_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, subrace_id: UUID) -> AppSubrace:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppSubrace]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[AppSubrace]:
        raise NotImplemented

    @abstractmethod
    async def save(self, subrace: AppSubrace) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, subrace_id: UUID) -> None:
        raise NotImplemented

from abc import ABC, abstractmethod
from uuid import UUID

from domain.subrace import Subrace


class SubraceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, subrace_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, subrace_id: UUID) -> Subrace:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Subrace]:
        raise NotImplemented

    @abstractmethod
    async def create(self, subrace: Subrace) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, subrace: Subrace) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, subrace_id: UUID) -> None:
        raise NotImplemented

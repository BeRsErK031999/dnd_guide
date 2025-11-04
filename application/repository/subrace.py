from abc import ABC, abstractmethod
from uuid import UUID

from domain.subrace.subrace import Subrace


class SubraceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_subrace_of_id_exist(self, subrace_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_subrace_of_id(self, subrace_id: UUID) -> Subrace:
        raise NotImplemented

    @abstractmethod
    async def save(self, subrace: Subrace) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, subrace_id: UUID) -> None:
        raise NotImplemented

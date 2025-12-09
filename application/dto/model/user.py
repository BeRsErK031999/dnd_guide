from dataclasses import dataclass
from uuid import UUID

from domain.user import User

__all__ = ["AppUser"]


@dataclass
class AppUser:
    user_id: UUID

    @staticmethod
    def from_domain(domain_user: User) -> "AppUser":
        return AppUser(user_id=domain_user.user_id())

    def to_domain(self) -> User:
        return User(user_id=self.user_id)

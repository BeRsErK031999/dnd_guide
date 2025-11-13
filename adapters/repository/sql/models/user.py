from adapters.repository.sql.models.base import Base
from domain.user import User


class UserModel(Base):
    __tablename__ = "user"

    def to_domain(self) -> User:
        return User(user_id=self.id)

    @staticmethod
    def from_domain(domain_user: User) -> UserModel:
        return UserModel(id=domain_user.user_id)

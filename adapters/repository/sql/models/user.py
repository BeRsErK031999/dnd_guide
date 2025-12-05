from adapters.repository.sql.models.base import Base
from application.dto.model.user import AppUser
from domain.user import User


class UserModel(Base):
    __tablename__ = "user"

    def to_app(self) -> AppUser:
        return AppUser(user_id=self.id)

    @staticmethod
    def from_app(domain_user: AppUser) -> "UserModel":
        return UserModel(id=domain_user.user_id)

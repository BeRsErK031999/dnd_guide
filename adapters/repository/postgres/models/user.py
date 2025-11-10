from adapters.repository.postgres.models.base import Base
from adapters.repository.postgres.models.mixin import Timestamp


class User(Timestamp, Base):
    __tablename__ = "user"

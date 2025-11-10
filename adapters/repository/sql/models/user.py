from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp


class User(Timestamp, Base):
    __tablename__ = "user"

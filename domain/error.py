from enum import Enum


class DomainErrorStatus(Enum):
    NOT_FOUND = 1
    INVALID_DATA = 2
    ACCESS = 3
    IDEMPOTENT = 4
    POLICY = 5
    INTERNAL = 100


class DomainError(Exception):
    def __init__(self, status: Enum, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.status = status
        self.msg = msg

    @classmethod
    def not_found(cls, msg: str) -> "DomainError":
        return cls(status=DomainErrorStatus.NOT_FOUND, msg=msg)

    @classmethod
    def invalid_data(cls, msg: str) -> "DomainError":
        return cls(status=DomainErrorStatus.INVALID_DATA, msg=msg)

    @classmethod
    def access(cls, msg: str) -> "DomainError":
        if len(msg) == 0:
            msg = "у вас недостаточно прав для совершения операции"
        return cls(status=DomainErrorStatus.ACCESS, msg=msg)

    @classmethod
    def idempotent(cls, msg: str) -> "DomainError":
        return cls(status=DomainErrorStatus.IDEMPOTENT, msg=msg)

    @classmethod
    def policy(cls, msg: str) -> "DomainError":
        return cls(status=DomainErrorStatus.POLICY, msg=msg)

    @classmethod
    def internal(cls, msg: str) -> "DomainError":
        return cls(status=DomainErrorStatus.INTERNAL, msg=msg)

from enum import Enum


class AppErrorStatus(Enum):
    NOT_FOUND = 1
    INVALID_DATA = 2
    ACCESS = 3
    IDEMPOTENT = 4
    POLICY = 5
    INTERNAL = 100


class AppError(Exception):
    def __init__(self, status: Enum, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.status = status
        self.msg = msg

    @classmethod
    def not_found(cls, msg: str) -> AppError:
        return cls(status=AppErrorStatus.NOT_FOUND, msg=msg)

    @classmethod
    def invalid_data(cls, msg: str) -> AppError:
        return cls(status=AppErrorStatus.INVALID_DATA, msg=msg)

    @classmethod
    def access(cls, msg: str) -> AppError:
        if len(msg) == 0:
            msg = "у вас недостаточно прав для совершения операции"
        return cls(status=AppErrorStatus.ACCESS, msg=msg)

    @classmethod
    def idempotent(cls, msg: str) -> AppError:
        return cls(status=AppErrorStatus.IDEMPOTENT, msg=msg)

    @classmethod
    def policy(cls, msg: str) -> AppError:
        return cls(status=AppErrorStatus.POLICY, msg=msg)

    @classmethod
    def internal(cls, msg: str) -> AppError:
        return cls(status=AppErrorStatus.INTERNAL, msg=msg)

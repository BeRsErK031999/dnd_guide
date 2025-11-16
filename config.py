import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_USER: str = os.getenv("DB_USER", "dnd_guide")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "dnd_guide")
    DB_NAME: str = os.getenv("DB_NAME", "dnd_guide")

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    ALLOWED_HOSTS: list[str] = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(
        ","
    )
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS", ("http://127.0.0.1:8000" ",http://localhost:8000")
    ).split(",")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


config = Config()

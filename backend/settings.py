from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode


class Settings(BaseSettings):
    """Read from environment variables of the same name, case-insensitive."""

    database_url: str
    build_environment: str = "prod"
    # Comma-separated, e.g. ALLOWED_ORIGINS=http://localhost:5173,https://x.com
    allowed_origins: Annotated[list[str], NoDecode] = ["*"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [o.strip() for o in value.split(",") if o.strip()]
        return value

    @property
    def is_local(self) -> bool:
        return self.build_environment == "local"


settings = Settings()

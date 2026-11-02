from datetime import datetime, timezone

from pydantic import field_validator
from sqlmodel import DateTime, Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    """Only the fields sent are changed."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("name")
    @classmethod
    def name_not_null(cls, value):
        # Omitting name keeps it; sending null would break the NOT NULL.
        if value is None:
            raise ValueError("name can't be null")
        return value


class ItemPublic(ItemBase):
    id: int
    created_at: datetime

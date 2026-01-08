from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class HNItemPydantic(BaseModel):
    id: int
    title: str
    url: Optional[str] = None
    text: Optional[str] = None
    created_at: datetime
    author: str
    points: int


class HNItem(Base):
    __tablename__ = "hn_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String)
    text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)

    def to_pydantic(self) -> HNItemPydantic:
        return HNItemPydantic(
            id=self.id,
            title=self.title,
            url=self.url,
            text=self.text,
            created_at=self.created_at,
            author=self.author,
            points=self.points,
        )

    @classmethod
    def from_pydantic(cls, pydantic_item: HNItemPydantic) -> "HNItem":
        return cls(
            id=pydantic_item.id,
            title=pydantic_item.title,
            url=pydantic_item.url,
            text=pydantic_item.text,
            created_at=pydantic_item.created_at,
            author=pydantic_item.author,
            points=pydantic_item.points,
        )

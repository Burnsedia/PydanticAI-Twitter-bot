from typing import List, Optional
import feedparser

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class RSSItemPydantic(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    published: Optional[str] = None


class RSSItem(Base):
    __tablename__ = "rss_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    published: Mapped[Optional[str]] = mapped_column(String)

    def to_pydantic(self) -> RSSItemPydantic:
        return RSSItemPydantic(
            title=self.title,
            url=self.url,
            description=self.description,
            published=self.published,
        )

    @classmethod
    def from_pydantic(cls, pydantic_item: RSSItemPydantic) -> "RSSItem":
        return cls(
            title=pydantic_item.title,
            url=pydantic_item.url,
            description=pydantic_item.description,
            published=pydantic_item.published,
        )

from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UserContentPydantic(BaseModel):
    source: str  # e.g., "blog", "github"
    url: str
    title: Optional[str] = None
    content: str
    summary: Optional[str] = None


class UserContent(Base):
    __tablename__ = "user_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)

    def to_pydantic(self) -> UserContentPydantic:
        return UserContentPydantic(
            source=self.source,
            url=self.url,
            title=self.title,
            content=self.content,
            summary=self.summary,
        )

    @classmethod
    def from_pydantic(cls, pydantic_content: UserContentPydantic) -> "UserContent":
        return cls(
            source=pydantic_content.source,
            url=pydantic_content.url,
            title=pydantic_content.title,
            content=pydantic_content.content,
            summary=pydantic_content.summary,
        )

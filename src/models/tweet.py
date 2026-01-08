from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class TweetPydantic(BaseModel):
    text: str
    thread_position: int = 0
    thread_id: Optional[str] = None
    status: str = "pending"  # pending, posted, failed


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    thread_position: Mapped[int] = mapped_column(Integer, default=0)
    thread_id: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")

    def to_pydantic(self) -> TweetPydantic:
        return TweetPydantic(
            text=self.text,
            thread_position=self.thread_position,
            thread_id=self.thread_id,
            status=self.status,
        )

    @classmethod
    def from_pydantic(cls, pydantic_tweet: TweetPydantic) -> "Tweet":
        return cls(
            text=pydantic_tweet.text,
            thread_position=pydantic_tweet.thread_position,
            thread_id=pydantic_tweet.thread_id,
            status=pydantic_tweet.status,
        )

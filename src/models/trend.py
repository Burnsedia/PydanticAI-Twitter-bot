from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class TrendPydantic(BaseModel):
    name: str
    tweet_volume: Optional[int] = None
    woeid: int


class Trend(Base):
    __tablename__ = "trends"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tweet_volume: Mapped[Optional[int]] = mapped_column(Integer)
    woeid: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_pydantic(self) -> TrendPydantic:
        return TrendPydantic(
            name=self.name,
            tweet_volume=self.tweet_volume,
            woeid=self.woeid,
        )

    @classmethod
    def from_pydantic(cls, pydantic_trend: TrendPydantic) -> "Trend":
        return cls(
            name=pydantic_trend.name,
            tweet_volume=pydantic_trend.tweet_volume,
            woeid=pydantic_trend.woeid,
        )

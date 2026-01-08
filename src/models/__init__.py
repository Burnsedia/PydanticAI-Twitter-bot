from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .hn import HNItem
from .trend import Trend
from .tweet import Tweet
from .user_content import UserContent

from abc import ABC, abstractmethod
from typing import List, TypeVar

T = TypeVar("T")


class Fetcher(ABC):
    @abstractmethod
    async def fetch(self) -> List[T]:
        """Fetch data and return a list of items."""
        pass

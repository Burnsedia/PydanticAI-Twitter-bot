import aiohttp
from datetime import datetime
from typing import List

from ..models.hn import HNItemPydantic
from .base import Fetcher


class HNFetcher(Fetcher):
    def __init__(self, top_limit: int = 30):
        self.top_limit = top_limit

    async def fetch(self) -> List[HNItemPydantic]:
        async with aiohttp.ClientSession() as session:
            # Get top story IDs
            async with session.get("https://hacker-news.firebaseio.com/v0/topstories.json") as resp:
                ids = await resp.json()
                ids = ids[: self.top_limit]

            items = []
            for item_id in ids:
                async with session.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                ) as resp:
                    data = await resp.json()
                    if data:
                        # Convert timestamp to datetime
                        created_at = datetime.fromtimestamp(data.get("time", 0))
                        item = HNItemPydantic(
                            id=data["id"],
                            title=data["title"],
                            url=data.get("url"),
                            text=data.get("text"),
                            created_at=created_at,
                            author=data["by"],
                            points=data.get("score", 0),
                        )
                        items.append(item)
            return items

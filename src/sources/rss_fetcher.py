from typing import List
import feedparser

from ..models.rss import RSSItemPydantic
from .base import Fetcher


class RSSFetcher(Fetcher):
    def __init__(self, urls: List[str]):
        self.urls = urls

    async def fetch(self) -> List[RSSItemPydantic]:
        items = []
        for url in self.urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                item = RSSItemPydantic(
                    title=entry.title,
                    url=entry.link,
                    description=getattr(entry, "description", None),
                    published=getattr(entry, "published", None),
                )
                items.append(item)
        return items

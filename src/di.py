from typing import Dict, Type
from ..config import settings
from .sources.base import Fetcher
from .sources.hn_fetcher import HNFetcher
from .sources.twitter_fetcher import TwitterFetcher
from .sources.rss_fetcher import RSSFetcher


class SourceRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[Fetcher]] = {}

    def register(self, name: str, fetcher_class: Type[Fetcher]):
        self._registry[name] = fetcher_class

    def get_fetcher(self, name: str) -> Fetcher:
        if name == "hn":
            return HNFetcher()
        elif name == "twitter":
            return TwitterFetcher()
        elif name == "rss":
            urls = settings.rss_feeds.split(",") if settings.rss_feeds else []
            return RSSFetcher(urls)
        else:
            raise ValueError(f"Unknown fetcher: {name}")


registry = SourceRegistry()

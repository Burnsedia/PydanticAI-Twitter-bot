from typing import List
import tweepy

from ..config import settings
from ..models.trend import TrendPydantic
from .base import Fetcher


class TwitterFetcher(Fetcher[TrendPydantic]):
    def __init__(self, woeid: int = 1):  # 1 = Worldwide
        self.woeid = woeid
        self.client = tweepy.Client(
            bearer_token=settings.twitter_bearer_token,
            consumer_key=settings.twitter_consumer_key,
            consumer_secret=settings.twitter_consumer_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret,
        )

    async def fetch(self) -> List[TrendPydantic]:
        # Note: Tweepy trends API is sync, wrap in async
        trends = self.client.get_place_trends(id=self.woeid)
        items = []
        for trend in trends.data:
            item = TrendPydantic(name=trend.name, tweet_volume=trend.tweet_volume, woeid=self.woeid)
            items.append(item)
        return items

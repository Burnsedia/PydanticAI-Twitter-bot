from typing import List
from pydantic import BaseModel
import pydantic_ai

from ..config import settings
from ..di import registry
from ..database import get_db
from ..models.hn import HNItemPydantic, HNItem
from ..models.trend import TrendPydantic, Trend
from ..models.rss import RSSItemPydantic, RSSItem


class HotTopic(BaseModel):
    title: str
    source: str
    url: str
    virality_score: float


class ResearchAgent:
    def __init__(self):
        self.agent = pydantic_ai.Agent(
            "openai:gpt-4o-mini",
            system_prompt="You are a research assistant for viral Twitter content. Analyze HN stories, Twitter trends, and RSS feeds to identify topics with high engagement potential (10k+ likes/retweets). Score based on points, volume, and relevance.",
            result_type=List[HotTopic],
        )

    async def run_research(self) -> List[HotTopic]:
        # Fetch data
        hn_fetcher = registry.get_fetcher("hn")
        twitter_fetcher = registry.get_fetcher("twitter")
        rss_fetcher = registry.get_fetcher("rss")

        hn_data = await hn_fetcher.fetch()
        twitter_data = await twitter_fetcher.fetch()
        rss_data = await rss_fetcher.fetch()

        # Save to DB
        async for session in get_db():
            for item in hn_data:
                db_item = HNItem.from_pydantic(item)
                session.add(db_item)
            for item in twitter_data:
                db_item = Trend.from_pydantic(item)
                session.add(db_item)
            for item in rss_data:
                db_item = RSSItem.from_pydantic(item)
                session.add(db_item)
            await session.commit()

        # Analyze for viral topics
        hot_topics = []
        for hn in hn_data:
            if hn.points >= settings.viral_points_threshold:
                score = hn.points / 100  # Simple score
                for trend in twitter_data:
                    if trend.tweet_volume and trend.tweet_volume >= settings.viral_volume_threshold:
                        # Check keyword overlap (simple)
                        if any(word.lower() in hn.title.lower() for word in trend.name.split()):
                            score += trend.tweet_volume / 10000
                hot_topics.append(
                    HotTopic(
                        title=hn.title,
                        source="HN",
                        url=hn.url or f"https://news.ycombinator.com/item?id={hn.id}",
                        virality_score=min(score, 10),  # Cap at 10
                    )
                )

        # Sort by score
        hot_topics.sort(key=lambda x: x.virality_score, reverse=True)
        return hot_topics[:5]  # Top 5

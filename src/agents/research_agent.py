from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent

from ..config import settings
from ..database import get_db
from ..models.hn import HNItemPydantic, HNItem
from ..models.trend import TrendPydantic, Trend
from ..models.rss import RSSItemPydantic, RSSItem


class HotTopic(BaseModel):
    title: str
    source: str
    url: str
    virality_score: float


research_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=f"You are a research assistant for viral Twitter content. Analyze provided HN stories, Twitter trends, and RSS feeds. Identify topics with high engagement potential (points >= {settings.viral_points_threshold}, volume >= {settings.viral_volume_threshold}). Score based on points, volume, and keyword overlap. Return top 5 hot topics.",
)


async def run_research() -> List[HotTopic]:
    from ..di import container

    # Get fetchers from DI
    hn_fetcher = container.hn_fetcher()
    twitter_fetcher = container.twitter_fetcher()
    rss_fetcher = container.rss_fetcher()

    hn_data = await hn_fetcher.fetch()
    twitter_data = await twitter_fetcher.fetch()
    rss_data = await rss_fetcher.fetch()

    # Save to DB
    db_session = container.db_session()
    async with db_session as session:
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

    # Prepare data for agent
    data_summary = (
        f"HN: {', '.join([f'{item.title} ({item.points} points)' for item in hn_data])}\n"
    )
    data_summary += f"Trends: {', '.join([f'{item.name} ({item.tweet_volume or 0})' for item in twitter_data])}\n"
    data_summary += f"RSS: {', '.join([item.title for item in rss_data])}"

    result = await research_agent.run(
        f"Analyze this data and identify viral topics:\n{data_summary}", result_type=List[HotTopic]
    )
    return result.data

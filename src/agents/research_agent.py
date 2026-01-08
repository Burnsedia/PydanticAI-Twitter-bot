from typing import List
from pydantic import BaseModel
from pydantic_ai import Agent, tool

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


@tool
async def fetch_hn() -> str:
    """Fetch Hacker News stories."""
    hn_fetcher = registry.get_fetcher("hn")
    hn_data = await hn_fetcher.fetch()
    async for session in get_db():
        for item in hn_data:
            db_item = HNItem.from_pydantic(item)
            session.add(db_item)
        await session.commit()
    return f"HN Stories: {', '.join([f'{item.title} ({item.points} pts)' for item in hn_data])}"


@tool
async def fetch_trends() -> str:
    """Fetch Twitter trends."""
    twitter_fetcher = registry.get_fetcher("twitter")
    twitter_data = await twitter_fetcher.fetch()
    async for session in get_db():
        for item in twitter_data:
            db_item = Trend.from_pydantic(item)
            session.add(db_item)
        await session.commit()
    return f"Twitter Trends: {', '.join([f'{item.name} ({item.tweet_volume or 0} vol)' for item in twitter_data])}"


@tool
async def fetch_rss() -> str:
    """Fetch RSS feeds."""
    rss_fetcher = registry.get_fetcher("rss")
    rss_data = await rss_fetcher.fetch()
    async for session in get_db():
        for item in rss_data:
            db_item = RSSItem.from_pydantic(item)
            session.add(db_item)
        await session.commit()
    return f"RSS Items: {', '.join([item.title for item in rss_data])}"


research_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=f"You are a research assistant for viral Twitter content. Use tools to fetch data from HN, Twitter, and RSS. Identify topics with high engagement potential (HN points >= {settings.viral_points_threshold}, Twitter volume >= {settings.viral_volume_threshold}). Score based on points, volume, and keyword overlap. Return top 5 hot topics.",
    result_type=List[HotTopic],
    tools=[fetch_hn, fetch_trends, fetch_rss],
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
    async with db_session() as session:  # Assuming AsyncSessionLocal is callable
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
        f"Analyze this data and identify viral topics:\n{data_summary}"
    )
    return result.data

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine

from .config import Settings, settings
from .database import AsyncSessionLocal
from .sources.hn_fetcher import HNFetcher
from .sources.twitter_fetcher import TwitterFetcher
from .sources.rss_fetcher import RSSFetcher
from .agents.research_agent import research_agent
from .agents.opinion_agent import opinion_agent
from .agents.tweet_agent import tweet_agent

from .services.scraper import ScraperService
from .services.scheduler import SchedulerService


class Container(containers.DeclarativeContainer):
    # Config
    config = providers.Singleton(Settings)

    # Database
    db_engine = providers.Singleton(
        create_async_engine, url=config.provided.database_url, echo=True
    )
    db_session = providers.Singleton(AsyncSessionLocal)

    # Fetchers
    hn_fetcher = providers.Singleton(HNFetcher)
    twitter_fetcher = providers.Singleton(TwitterFetcher)
    rss_fetcher = providers.Factory(
        RSSFetcher,
        urls=providers.Callable(
            lambda rss_feeds: rss_feeds.split(",") if rss_feeds else [], config.provided.rss_feeds
        ),
    )

    # Agents
    research_agent_provider = providers.Object(research_agent)
    opinion_agent_provider = providers.Object(opinion_agent)
    tweet_agent_provider = providers.Object(tweet_agent)

    # Services
    scraper_service = providers.Singleton(ScraperService)
    scheduler_service = providers.Singleton(SchedulerService)


container = Container()

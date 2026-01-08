import asyncio
import logging
from src.di import container
from src.database import create_tables

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_bot_cycle():
    """Run one full bot cycle: scrape, research, generate, post."""
    try:
        # Scrape user content
        scraper = container.scraper_service()
        async with scraper:
            blog_content = await scraper.scrape_blog()
            github_content = await scraper.scrape_github()
        logger.info(f"Scraped {len(blog_content)} blog items, {len(github_content)} GitHub items")

        # Research viral topics
        from src.agents.research_agent import run_research

        hot_topics = await run_research()
        logger.info(f"Found {len(hot_topics)} hot topics")

        # For each topic, generate and post
        for topic in hot_topics[:2]:  # Limit for testing
            # Generate opinion
            from src.agents.opinion_agent import generate_opinions

            opinions = await generate_opinions([topic.title])
            opinion = opinions[0] if opinions else None

            if opinion:
                # Generate tweet thread
                from src.agents.tweet_agent import generate_thread

                tweet_thread = await generate_thread(topic, opinion)

                # Post thread
                posting_agent = container.posting_agent()
                posted_ids = await posting_agent.post_thread(tweet_thread.tweets)
                logger.info(f"Posted thread with IDs: {posted_ids}")
    except Exception as e:
        logger.error(f"Error in bot cycle: {e}")


async def main():
    # Wire dependencies
    container.wire(modules=["src.agents", "src.services", "src.sources"])

    logger.info("Starting PydanticAI Twitter Bot...")

    # Create DB tables
    await create_tables()
    logger.info("DB tables created.")

    # Run initial cycle
    await run_bot_cycle()

    # Schedule recurring cycles
    scheduler = container.scheduler_service()
    scheduler.schedule_task(run_bot_cycle)

    # Start scheduler (runs indefinitely)
    await scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())

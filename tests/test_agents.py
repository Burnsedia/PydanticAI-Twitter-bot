import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel
from src.agents.research_agent import HotTopic
from src.agents.tweet_agent import TweetThread, Tweet


class MockAgentRunResult(BaseModel):
    data: list


@pytest.mark.asyncio
async def test_research_agent():
    # Mock dependencies
    with (
        patch("src.agents.research_agent.container") as mock_container,
        patch("src.agents.research_agent.research_agent") as mock_agent,
    ):
        # Mock fetchers
        mock_hn = AsyncMock()
        mock_hn.fetch.return_value = []
        mock_twitter = AsyncMock()
        mock_twitter.fetch.return_value = []
        mock_rss = AsyncMock()
        mock_rss.fetch.return_value = []

        mock_container.hn_fetcher.return_value = mock_hn
        mock_container.twitter_fetcher.return_value = mock_twitter
        mock_container.rss_fetcher.return_value = mock_rss
        mock_container.db_session.return_value = AsyncMock()

        # Mock agent run
        mock_agent.run.return_value = MockAgentRunResult(
            data=[
                HotTopic(
                    title="Test Topic", source="HN", url="http://example.com", virality_score=5.0
                )
            ]
        )

        from src.agents.research_agent import run_research

        topics = await run_research()

        assert len(topics) == 1
        assert topics[0].title == "Test Topic"


@pytest.mark.asyncio
async def test_tweet_agent():
    with patch("src.agents.tweet_agent.tweet_agent") as mock_agent:
        mock_agent.run.return_value = MockAgentRunResult(
            data=TweetThread(tweets=[Tweet(text="Test tweet", position=0)])
        )

        from src.agents.tweet_agent import generate_thread
        from src.agents.research_agent import HotTopic
        from src.agents.opinion_agent import Opinion

        topic = HotTopic(title="Topic", source="HN", url="http://example.com", virality_score=1.0)
        opinion = Opinion(topic="Topic", opinion="Good opinion", style_notes="Confident")

        thread = await generate_thread(topic, opinion)

        assert len(thread.tweets) == 1
        assert thread.tweets[0].text == "Test tweet"


@pytest.mark.asyncio
async def test_opinion_agent():
    with (
        patch("src.agents.opinion_agent.opinion_agent") as mock_agent,
        patch("src.agents.opinion_agent.get_db") as mock_get_db,
    ):
        mock_get_db.return_value = AsyncMock()
        mock_agent.run.return_value = MockAgentRunResult(
            data=[{"topic": "Topic", "opinion": "Test opinion", "style_notes": "Style"}]
        )

        from src.agents.opinion_agent import generate_opinions

        opinions = await generate_opinions(["Topic"])

        assert len(opinions) == 1
        assert opinions[0]["topic"] == "Topic"

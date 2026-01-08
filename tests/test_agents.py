import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel


class MockAgentRunResult(BaseModel):
    data: list


@pytest.mark.asyncio
async def test_research_agent_with_tools():
    with (
        patch("src.agents.research_agent.container") as mock_container,
        patch("src.agents.research_agent.research_agent") as mock_agent,
        patch("src.agents.research_agent.get_db") as mock_get_db,
        patch("src.agents.research_agent.HotTopic") as mock_hot_topic,
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
        mock_get_db.return_value = AsyncMock()

        # Mock agent run
        mock_result = AsyncMock()
        mock_result.data = [
            {
                "title": "Test Topic",
                "source": "HN",
                "url": "http://example.com",
                "virality_score": 5.0,
            }
        ]
        mock_agent.run.return_value = mock_result

        from src.agents.research_agent import run_research

        topics = await run_research()

        assert len(topics) == 1
        assert topics[0]["title"] == "Test Topic"


@pytest.mark.asyncio
async def test_tweet_agent():
    with (
        patch("src.agents.tweet_agent.tweet_agent") as mock_agent,
        patch("src.agents.tweet_agent.TweetThread") as mock_thread,
        patch("src.agents.tweet_agent.Tweet") as mock_tweet,
    ):
        mock_tweet.return_value.text = "Test tweet"
        mock_tweet.return_value.position = 0
        mock_thread.return_value.tweets = [mock_tweet.return_value]
        mock_result = AsyncMock()
        mock_result.data = mock_thread.return_value
        mock_agent.run.return_value = mock_result

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
        patch("src.agents.opinion_agent.Opinion") as mock_opinion,
    ):
        mock_get_db.return_value = AsyncMock()
        mock_result = AsyncMock()
        mock_result.data = [{"topic": "Topic", "opinion": "Test opinion", "style_notes": "Style"}]
        mock_agent.run.return_value = mock_result

        from src.agents.opinion_agent import generate_opinions

        opinions = await generate_opinions(["Topic"])

        assert len(opinions) == 1
        assert opinions[0]["topic"] == "Topic"

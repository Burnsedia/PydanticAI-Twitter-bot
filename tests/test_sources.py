import pytest
from aioresponses import aioresponses
from unittest.mock import patch
from src.sources.hn_fetcher import HNFetcher
from src.sources.twitter_fetcher import TwitterFetcher
from src.sources.rss_fetcher import RSSFetcher


@pytest.mark.asyncio
async def test_hn_fetcher():
    with aioresponses() as m:
        # Mock HN API
        m.get("https://hacker-news.firebaseio.com/v0/topstories.json", payload=[1, 2])
        m.get(
            "https://hacker-news.firebaseio.com/v0/item/1.json",
            payload={"id": 1, "title": "Test Story", "score": 10, "by": "user", "time": 1640995200},
        )
        m.get(
            "https://hacker-news.firebaseio.com/v0/item/2.json",
            payload={
                "id": 2,
                "title": "Another Story",
                "score": 5,
                "by": "user2",
                "time": 1640995300,
            },
        )

        fetcher = HNFetcher()
        items = await fetcher.fetch()

        assert len(items) == 2
        assert items[0].title == "Test Story"
        assert items[0].points == 10


@pytest.mark.asyncio
async def test_twitter_fetcher():
    # Mock Tweepy
    fetcher = TwitterFetcher()
    mock_response = type("MockResponse", (), {"data": [{"name": "#Test", "tweet_volume": 1000}]})()
    with patch.object(fetcher.client, "get_place_trends", return_value=mock_response):
        items = await fetcher.fetch()

    assert len(items) == 1
    assert items[0].name == "#Test"
    assert items[0].tweet_volume == 1000


@pytest.mark.asyncio
async def test_rss_fetcher():
    # Mock feedparser
    import feedparser

    mock_entry = type(
        "MockEntry",
        (),
        {
            "title": "RSS Item 1",
            "link": "http://example.com/1",
            "description": "Desc",
            "published": "Mon, 01 Jan 2024 00:00:00 GMT",
        },
    )()

    original_parse = feedparser.parse
    feedparser.parse = lambda url: type("MockFeed", (), {"entries": [mock_entry]})()

    try:
        fetcher = RSSFetcher(["http://example.com/feed"])
        items = await fetcher.fetch()

        assert len(items) == 1
        assert items[0].title == "RSS Item 1"
    finally:
        feedparser.parse = original_parse

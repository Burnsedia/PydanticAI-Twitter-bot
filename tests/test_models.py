import pytest
from datetime import datetime
from src.models.hn import HNItemPydantic, HNItem
from src.models.trend import TrendPydantic, Trend
from src.models.tweet import TweetPydantic, Tweet
from src.models.user_content import UserContentPydantic, UserContent


def test_hn_item_pydantic():
    item = HNItemPydantic(
        id=1,
        title="Test Story",
        url="https://example.com",
        text="Test text",
        created_at=datetime.now(),
        author="testuser",
        points=10,
    )
    assert item.title == "Test Story"
    assert item.points == 10


def test_hn_item_conversion():
    pydantic_item = HNItemPydantic(
        id=1, title="Test", created_at=datetime.now(), author="user", points=5
    )
    db_item = HNItem.from_pydantic(pydantic_item)
    assert db_item.id == 1
    assert db_item.title == "Test"

    back = db_item.to_pydantic()
    assert back.title == "Test"


def test_trend_model():
    pydantic_trend = TrendPydantic(name="#Test", tweet_volume=1000, woeid=1)
    db_trend = Trend.from_pydantic(pydantic_trend)
    assert db_trend.name == "#Test"
    assert db_trend.tweet_volume == 1000


def test_tweet_model():
    pydantic_tweet = TweetPydantic(text="Hello world", thread_position=0, status="pending")
    db_tweet = Tweet.from_pydantic(pydantic_tweet)
    assert db_tweet.text == "Hello world"
    assert db_tweet.status == "pending"


def test_user_content_model():
    pydantic_content = UserContentPydantic(
        source="blog",
        url="https://blog.com",
        title="Blog Post",
        content="Content here",
        summary="Summary",
    )
    db_content = UserContent.from_pydantic(pydantic_content)
    assert db_content.source == "blog"
    assert db_content.title == "Blog Post"

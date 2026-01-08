import os
import pytest


@pytest.fixture(autouse=True)
def set_test_env():
    # Set test environment variables
    os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    os.environ.setdefault("OPENAI_API_KEY", "test_key")
    os.environ.setdefault("TWITTER_BEARER_TOKEN", "test")
    os.environ.setdefault("TWITTER_CONSUMER_KEY", "test")
    os.environ.setdefault("TWITTER_CONSUMER_SECRET", "test")
    os.environ.setdefault("TWITTER_ACCESS_TOKEN", "test")
    os.environ.setdefault("TWITTER_ACCESS_TOKEN_SECRET", "test")
    os.environ.setdefault("BLOG_URL", "https://example.com")
    os.environ.setdefault("GITHUB_USERNAME", "test")
    os.environ.setdefault("TWITTER_HANDLE", "@test")
    os.environ.setdefault("TWEET_FREQUENCY_HOURS", "4")
    os.environ.setdefault("MAX_THREAD_LENGTH", "3")
    os.environ.setdefault("VIRAL_POINTS_THRESHOLD", "200")
    os.environ.setdefault("VIRAL_VOLUME_THRESHOLD", "10000")
    os.environ.setdefault("RSS_FEEDS", "https://example.com/feed")
    yield

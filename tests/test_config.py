from src.config import Settings


def test_settings_load():
    settings = Settings()
    assert settings.database_url == "sqlite+aiosqlite:///./test.db"
    assert settings.twitter_bearer_token == "test"  # From env


def test_settings_validation():
    # Test defaults
    settings = Settings()
    assert settings.tweet_frequency_hours == 4
    assert settings.viral_points_threshold == 200

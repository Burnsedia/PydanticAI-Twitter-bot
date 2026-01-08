from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Twitter API v2 credentials
    twitter_bearer_token: str = ""
    twitter_consumer_key: str = ""
    twitter_consumer_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_token_secret: str = ""

    # Database
    database_url: str = "sqlite:///./bot.db"

    # User content sources
    blog_url: str = ""
    github_username: str = ""
    twitter_handle: str = ""

    # Bot settings
    tweet_frequency_hours: int = 4
    max_thread_length: int = 3
    viral_points_threshold: int = 200
    viral_volume_threshold: int = 10000

    # RSS feeds
    rss_feeds: str = ""

    # OpenAI API
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

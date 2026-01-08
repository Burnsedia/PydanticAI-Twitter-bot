from src.di import container


def test_container_providers():
    config = container.config()
    assert config.database_url == "sqlite+aiosqlite:///./test.db"

    hn_fetcher = container.hn_fetcher()
    assert hn_fetcher is not None  # Instance created

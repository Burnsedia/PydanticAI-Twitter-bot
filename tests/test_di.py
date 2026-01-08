from unittest.mock import patch


def test_container_providers():
    with (
        patch("src.di.AsyncSessionLocal"),
        patch("src.di.create_async_engine"),
        patch("src.di.Settings") as mock_settings,
    ):
        mock_settings.return_value.database_url = "sqlite+aiosqlite:///./test.db"

        from src.di import container

        config = container.config()
        assert config.database_url == "sqlite+aiosqlite:///./test.db"

        hn_fetcher = container.hn_fetcher()
        assert hn_fetcher is not None  # Instance created

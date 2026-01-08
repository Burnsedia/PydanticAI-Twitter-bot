import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_create_tables():
    # Mock engine and session
    with (
        patch("src.database.engine") as mock_engine,
        patch("src.database.settings") as mock_settings,
    ):
        mock_settings.database_url = "sqlite+aiosqlite:///./test.db"
        mock_conn = AsyncMock()
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.run_sync = AsyncMock()

        from src.database import create_tables

        await create_tables()
        mock_conn.run_sync.assert_called_once()

import pytest
from unittest.mock import patch, AsyncMock
from src.database import create_tables


@pytest.mark.asyncio
async def test_create_tables():
    # Mock engine and session
    with patch("src.database.engine") as mock_engine:
        mock_conn = AsyncMock()
        mock_engine.begin.return_value.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.run_sync = AsyncMock()

        await create_tables()
        mock_conn.run_sync.assert_called_once()

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_full_bot_cycle():
    # Mock all components
    with (
        patch("src.main.container") as mock_container,
        patch("src.main.run_research") as mock_research,
        patch("src.main.generate_opinions") as mock_opinions,
        patch("src.main.generate_thread") as mock_thread,
        patch("src.main.post_thread_via_agent") as mock_post,
    ):
        # Set up mocks
        mock_research.return_value = [{"title": "Test Topic"}]
        mock_opinions.return_value = [{"opinion": "Good"}]
        mock_thread.return_value = {"tweets": [{"text": "Tweet", "position": 0}]}

        from src.main import run_bot_cycle

        await run_bot_cycle()

        mock_research.assert_called_once()
        mock_opinions.assert_called_once()
        mock_thread.assert_called_once()
        mock_post.assert_called_once()

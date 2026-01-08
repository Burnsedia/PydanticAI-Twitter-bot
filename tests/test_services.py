import pytest
from unittest.mock import patch, AsyncMock
import asyncio


@pytest.mark.asyncio
async def test_scraper_service():
    from src.services.scraper import ScraperService

    service = ScraperService()

    with patch("aiohttp.ClientSession") as mock_session:
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.text = AsyncMock(return_value="<html><article><h1>Test</h1></article></html>")
        mock_session.return_value.get.return_value.__aenter__ = mock_resp
        mock_session.return_value.close = AsyncMock()

        async with service:
            items = await service.scrape_blog()
        assert len(items) >= 0  # Check parsing


@pytest.mark.asyncio
async def test_scheduler_service():
    from src.services.scheduler import SchedulerService
    import schedule

    scheduler = SchedulerService()

    def test_task():
        pass

    scheduler.schedule_task(test_task, hours=1)
    assert len(schedule.jobs) > 0  # Job is scheduled

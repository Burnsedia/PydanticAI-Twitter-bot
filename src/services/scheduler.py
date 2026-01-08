import asyncio
import schedule
from typing import Callable, Optional

from ..config import settings


class SchedulerService:
    def __init__(self):
        self.running = False
        self.job: Optional[schedule.Job] = None

    def schedule_task(self, task: Callable[[], None], hours: Optional[int] = None):
        """Schedule a task to run every X hours."""
        if hours is None:
            hours = settings.tweet_frequency_hours

        self.job = schedule.every(hours).hours.do(task)
        print(f"Scheduled task to run every {hours} hours")

    async def start(self):
        """Start the scheduler loop."""
        self.running = True
        print("Scheduler started")

        while self.running:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.job:
            schedule.cancel_job(self.job)
        print("Scheduler stopped")

    async def run_once(self, task: Callable[[], None]):
        """Run the task once (for testing)."""
        await asyncio.get_event_loop().run_in_executor(None, task)

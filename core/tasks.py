import logging
from typing import Dict, Any, List, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TaskManager:
    """
    Handles background tasks, reminders, and autonomous operations.
    Supports persistent and one-time scheduled jobs.
    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler(
            jobstores={'default': MemoryJobStore()},
            job_defaults={'misfire_grace_time': 10}
        )
        self.running = False

    def start(self):
        """Starts the background task scheduler."""
        if not self.running:
            self.scheduler.start()
            self.running = True
            logger.info("Task Manager started successfully.")

    def shutdown(self):
        """Stops the scheduler."""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            logger.info("Task Manager shut down.")

    def add_reminder(self, user_id: int, text: str, delay_minutes: int, callback: Callable):
        """Schedules a one-time reminder."""
        run_at = datetime.now() + timedelta(minutes=delay_minutes)
        job_id = f"reminder_{user_id}_{int(run_at.timestamp())}"
        
        self.scheduler.add_job(
            callback,
            'date',
            run_date=run_at,
            args=[user_id, text],
            id=job_id
        )
        logger.info(f"Scheduled reminder for {user_id} at {run_at}")
        return job_id

    def add_recurring_task(self, task_id: str, interval_minutes: int, callback: Callable, args: List = None):
        """Schedules a recurring task."""
        self.scheduler.add_job(
            callback,
            'interval',
            minutes=interval_minutes,
            args=args or [],
            id=task_id,
            replace_existing=True
        )
        logger.info(f"Scheduled recurring task {task_id} every {interval_minutes}m")

    def cancel_task(self, job_id: str):
        """Removes a scheduled task."""
        try:
            self.scheduler.remove_job(job_id)
            return True
        except Exception:
            return False

    def get_user_tasks(self, user_id: int) -> List[Dict[str, Any]]:
        """Returns a list of active tasks for a specific user."""
        jobs = self.scheduler.get_jobs()
        user_jobs = []
        for job in jobs:
            if str(user_id) in job.id:
                user_jobs.append({
                    "id": job.id,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None
                })
        return user_jobs

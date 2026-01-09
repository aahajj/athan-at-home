import time
import os
import logging
import paths
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler

from calendar_service import fetch_calendar_from_mawaqit
from scheduler_service import schedule_today_prayers
    
MASJID_ID = "massjid-ID"  # Replace with actual masjid ID

os.makedirs(paths.OUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(
            paths.LOG_PATH,
            maxBytes=1_000_000,
            backupCount=5,
        )
    ],
)

logger = logging.getLogger(__name__)


def main():

    scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
    scheduler.start()

    # Best-effort calendar refresh at startup
    try:
        fetch_calendar_from_mawaqit(MASJID_ID)
    except Exception as e:
        logger.error(f"Calendar refresh failed at startup: {e}")

    # Schedule today's prayers
    schedule_today_prayers(scheduler)

    # Refresh calendar monthly
    scheduler.add_job(
        fetch_calendar_from_mawaqit,
        "cron",
        day=1,
        hour=0,
        minute=5,
        args=[MASJID_ID],
    )

    # Reschedule prayers daily
    scheduler.add_job(
        schedule_today_prayers,
        "cron",
        hour=0,
        minute=1,
        args=[scheduler],
    )

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()

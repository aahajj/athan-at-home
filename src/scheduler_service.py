import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from calendar_reader import get_today_prayer_times
from player import play_athan

logger = logging.getLogger(__name__)


def schedule_today_prayers(scheduler: BackgroundScheduler) -> None:
    times = get_today_prayer_times()
    today = datetime.today()

    for t in times:
        run_at = datetime.combine(today.date(), t)
        if run_at > datetime.now():
            scheduler.add_job(play_athan, "date", run_date=run_at)
            logger.info(f"Scheduled Athan at {run_at}")

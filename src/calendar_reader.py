import os
import json
from paths import CALENDAR_PATH
from datetime import date, datetime


def get_today_prayer_times():
    with open(CALENDAR_PATH) as f:
        data = json.load(f)

    today = date.today()
    month_key = today.month - 1
    day_key = str(today.day)

    try:
        prayer_times = data[month_key][day_key]
    except KeyError:
        raise RuntimeError(f"No prayer data for {today.isoformat()}")

    if len(prayer_times) < 5:
        raise RuntimeError("Unexpected prayer format")

    prayers = [t for i, t in enumerate(prayer_times) if i != 1]
    return [datetime.strptime(t, "%H:%M").time() for t in prayers]
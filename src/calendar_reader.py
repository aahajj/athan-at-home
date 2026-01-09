import os
import json
from paths import CALENDAR_PATH
from datetime import date, datetime


def get_today_prayer_times():
    """
    Read today's prayer times from the local calendar file.
    
    Returns:
        list: Prayer times as datetime.time objects (excludes sunrise)
        
    Raises:
        FileNotFoundError: If calendar file doesn't exist
        RuntimeError: If calendar data is invalid or corrupted
    """
    if not os.path.exists(CALENDAR_PATH):
        raise FileNotFoundError(f"Calendar file not found at {CALENDAR_PATH}")
    
    try:
        with open(CALENDAR_PATH) as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        raise RuntimeError(f"Failed to read calendar file: {e}") from e

    today = date.today()
    month_key = today.month - 1
    day_key = str(today.day)

    try:
        prayer_times = data[month_key][day_key]
    except KeyError:
        raise RuntimeError(f"No prayer data for {today.isoformat()}")

    if len(prayer_times) < 5:
        raise RuntimeError("Unexpected prayer format")

    # Exclude sunrise (index 1)
    prayers = [t for i, t in enumerate(prayer_times) if i != 1]
    return [datetime.strptime(t, "%H:%M").time() for t in prayers]
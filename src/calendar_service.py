import json
import os
import re
import logging
import requests
from paths import CALENDAR_PATH, CALENDAR_TMP_PATH
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def validate_calendar(calendar) -> None:
    """
    Validate the structure and content of the calendar data.
    
    Args:
        calendar: List of 12 monthly dictionaries containing prayer times
        
    Raises:
        ValueError: If calendar structure or data is invalid
    """
    if not isinstance(calendar, list):
        raise ValueError("Calendar must be a list")

    if len(calendar) != 12:
        raise ValueError("Calendar must contain 12 months")

    for month_index, month in enumerate(calendar):
        if not isinstance(month, dict):
            raise ValueError(f"Month {month_index} must be a dict")

        for day, prayers in month.items():
            if not isinstance(day, str) or not day.isdigit():
                raise ValueError(f"Invalid day key: {day}")

            if not isinstance(prayers, list):
                raise ValueError(f"Prayer times for day {day} must be a list")

            if len(prayers) < 5:
                raise ValueError(f"Day {day} has too few prayer times")

            for t in prayers:
                if not isinstance(t, str) or not TIME_PATTERN.match(t):
                    raise ValueError(f"Invalid time format: {t}")
        

def fetch_calendar_from_mawaqit(masjid_id: str) -> None:
    """
    Fetch monthly prayer calendar from Mawaqit and persist locally.
    
    Args:
        masjid_id: The unique identifier for the masjid on Mawaqit
        
    Raises:
        requests.RequestException: If network request fails
        ValueError: If calendar data is invalid
        RuntimeError: If calendar data cannot be parsed
    """
    url = f"https://mawaqit.net/de/m/{masjid_id}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch calendar from Mawaqit: {e}") from e

    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", string=re.compile(r"var confData ="))

    if not script:
        raise RuntimeError("confData script not found in page")

    match = re.search(r"var confData = (.*?);", script.string, re.DOTALL)
    if not match:
        raise RuntimeError("Failed to parse confData from script")

    try:
        conf_data = json.loads(match.group(1))
        calendar = conf_data["calendar"]
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to extract calendar from confData: {e}") from e

    # Validate calendar before replacing the existing one
    try:
        validate_calendar(calendar)
    except ValueError as e:
        logger.error(f"Invalid calendar data: {e}")
        raise
    
    with open(CALENDAR_TMP_PATH, "w") as f:
        json.dump(calendar, f)
    os.replace(CALENDAR_TMP_PATH, CALENDAR_PATH)
    logger.info("Calendar updated successfully")
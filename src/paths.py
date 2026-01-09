import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "out")

CALENDAR_PATH = os.path.join(OUT_DIR, "calendar.json")
CALENDAR_TMP_PATH = os.path.join(OUT_DIR, "calendar.json.tmp")
LOG_PATH = os.path.join(OUT_DIR, "athan.log")

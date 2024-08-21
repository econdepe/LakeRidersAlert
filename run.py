from datetime import datetime
import sqlite3
from threading import Timer
from zoneinfo import ZoneInfo

from .constants import POLLING_INTERVAL, DB_NAME
from .helpers.browser import create_browser, navigate_to_calendar
from .helpers.calendar_entries import extract_calendar_entries, find_available_slots, write_calendar_entries_to_db
from .helpers.telegram_bot import notify_to_telegram

def run_once(browser=None):
    if browser is None:
        browser = create_browser()
    navigate_to_calendar(browser)

    calendar_entries = extract_calendar_entries(browser)
    available_slots = find_available_slots(browser)
    if available_slots is not None:
        notify_to_telegram(available_slots)
    write_calendar_entries_to_db(calendar_entries)

'''
    Polling should be run only between 7 and midnight during weekdays
'''
def run_once_conditionally(browser=None):
    now = datetime.now(ZoneInfo('Europe/Zurich'))
    if now.hour >= 7 and now.weekday() < 6:
        run_once()

def run_in_loop():
    t = Timer(POLLING_INTERVAL, run_once_conditionally)

if __name__ == '__main__':
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar(
            datetime TEXT
            , members TEXT
        )
    ''')

    conn.commit()
    conn.close()
    run_in_loop()

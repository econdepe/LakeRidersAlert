from datetime import datetime
from threading import Timer
from zoneinfo import ZoneInfo

from ..constants import POLLING_INTERVAL
from ..helpers.browser import create_browser, navigate_to_calendar
from ..helpers.calendar_entries import extract_calendar_entries, find_available_slots, write_calendar_entries_to_db
from ..helpers.telegram_bot import notify_to_telegram

def run_once(browser=None):
    if browser is None:
        browser = create_browser()
    navigate_to_calendar(browser)

    calendar_entries = extract_calendar_entries(browser)
    available_slots = find_available_slots(calendar_entries)
    if available_slots is not None:
        notify_to_telegram(available_slots)
    write_calendar_entries_to_db(calendar_entries)

'''
    Polling should be run only between 7am and midnight during weekdays
'''
def run_once_conditionally(browser=None):
    now = datetime.now(ZoneInfo('Europe/Zurich'))
    if now.hour >= 7 and now.weekday() < 6:
        run_once(browser)

def run_in_loop():
    run_once_conditionally()
    t = Timer(POLLING_INTERVAL, run_once_conditionally)
    t.start()

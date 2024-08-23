from datetime import datetime
from time import sleep
from zoneinfo import ZoneInfo

from ..constants import POLLING_INTERVAL, RUN_WITH_LOGS
from ..helpers.browser import create_browser, navigate_to_calendar
from ..helpers.calendar_entries import extract_calendar_entries, find_available_slots, write_calendar_entries_to_db
from ..helpers.telegram_bot import notify_to_telegram

def run_once(browser=None):
    if RUN_WITH_LOGS:
        message = f"Crawling lakeriders calendar on {datetime.now().strftime('%d %b, %H:%M')}"
        print(f"{'-'*len(message)}\n{message}\n...\n..\n.")

    browser_session = create_browser() if browser is None else browser
    navigate_to_calendar(browser_session)

    calendar_entries = extract_calendar_entries(browser_session)
    available_slots = find_available_slots(calendar_entries)
    if available_slots is not None:
        notify_to_telegram(available_slots)
    write_calendar_entries_to_db(calendar_entries)

    sleep(POLLING_INTERVAL)
    return browser_session

'''
    Polling should be run only between 7am and midnight during weekdays
'''
def run_once_conditionally(browser=None):
    now = datetime.now(ZoneInfo('Europe/Zurich'))
    if now.hour >= 7 and now.weekday() < 6:
        return run_once(browser)
    else:
        return None

def run_in_loop():
    browser = run_once_conditionally()
    while True:
        run_once_conditionally(browser)

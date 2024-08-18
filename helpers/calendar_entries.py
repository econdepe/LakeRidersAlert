import sqlite3

from selenium.webdriver.common.by import By

from ..constants import CANCELLED, FREE, DB_NAME



def extract_calendar_entries(browser):
    table_body = browser.find_element(By.CLASS_NAME, 'fc-body')
    week_dates = [table_body.find_element(By.CLASS_NAME, f"fc-{day}").get_attribute('data-date') for day in ['mon', 'tue', 'wed', 'thu', 'fri']]
    grid = table_body.find_element(By.CLASS_NAME, 'fc-content-skeleton')
    rows = [row.text.split('\n') for row in grid.find_elements(By.TAG_NAME, 'tr')]

    '''
        We store the calendar entries in a dictionary { [key]: value }, where:
            * key: str
                Date + time of the session in ISO format. E.g.: '2024-08-12T18:00:00'
            * value: str.
                Names of the participants of the session, separated by commas.
                If a session has been cancelled, the name used is 'CANCELLED'
                If a session is free, the name used is 'FREE
                E.g.: 'Bond J.,Norbert E.,FREE,CANCELLED'
    '''
    calendar_entries = {}


    for row in rows:
        for i, entry in enumerate(row):
            # Entries have the format '18:00 Bond J.'
            time = entry[:5]
            name = entry[6:]
            if name == 'Session annulée':
                name = CANCELLED
            elif name == 'Place disponible':
                name = FREE
            date = week_dates[i]
            datetime = f"{date}T{time}:00"
            if datetime in calendar_entries:
                calendar_entries[datetime] += f",{name}"
            else:
                calendar_entries[datetime] = name

def write_calendar_entries_to_db(calendar_entries):
    conn = sqlite3.connect(f"wake_alert.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar(
            datetime TEXT
            , members TEXT
        )
    ''')

    for datetime in calendar_entries:
        cursor.execute('''
            SELECT members
            FROM calendar
            WHERE datetime = ?
        ''', (datetime,))
        old_members_array = cursor.fetchall()

        if len(old_members_array) == 0:
            # No previous entry exists
            cursor.execute('''
                INSERT INTO calendar (datetime, members)
                VALUES (?, ?)
            ''', (datetime, calendar_entries[datetime]))
        else:
            # Overwrite previous entry
            cursor.execute('''
                UPDATE calendar
                SET members = ?
                WHERE datetime = ?
            ''', (calendar_entries[datetime], datetime))

    conn.commit()
    cursor.close()

def count_slots_available(new_members: str, old_members: str) -> int:
    new_free_slots = new_members.count(FREE)
    old_free_slots = old_members.count(FREE)

    return max(new_free_slots - old_free_slots, 0)


def find_available_slots(calendar_entries):
    conn = sqlite3.connect(f"{DB_NAME}")
    cursor = conn.cursor()

    result = {}
    has_available_slots = False

    for datetime in calendar_entries:
        cursor.execute('''
            SELECT members
            FROM calendar
            WHERE datetime = ?
        ''', (datetime,))
        old_members = cursor.fetchone()[0]

        if (count := count_slots_available(calendar_entries[datetime], old_members)):
            has_available_slots = True
            result[datetime] = count

    cursor.close()

    return result if has_available_slots else None

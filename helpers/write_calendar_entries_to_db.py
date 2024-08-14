import sqlite3

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

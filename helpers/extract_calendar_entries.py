from . import constants
from selenium.webdriver.common.by import By

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
                E.g.: 'Bond J., Norbert E., CANCELLED, CANCELLED'
    '''
    calendar_entries = {}


    for row in rows:
        for i, entry in enumerate(row):
            # Entries have the format '18:00 Bond J.'
            time = entry[:5]
            name = entry[6:]
            if name == 'Session annulée':
                name = constants.CANCELLED
            date = week_dates[i]
            datetime = f"{date}T{time}:00"
            if datetime in calendar_entries:
                calendar_entries[datetime] += f", {name}"
            else:
                calendar_entries[datetime] = name

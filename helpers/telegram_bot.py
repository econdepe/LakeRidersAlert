from datetime import datetime

import requests

from ..constants import BOT_TOKEN as token, CHAT_ID as chat_id


def _format_day_(weekday):
    if weekday == 0:
        return 'Monday'
    elif weekday == 1:
        return 'Tuesday'
    elif weekday == 2:
        return 'Wednesday'
    elif weekday == 3:
        return 'Thursday'
    elif weekday == 4:
        return 'Friday'
    elif weekday == 5:
        return 'Saturday'
    elif weekday == 6:
        return 'Sunday'
    else:
        raise Exception('Unknown weekday value')

def _format_n_slots_(n):
    if n == 1:
        return '1 slot'
    else:
        return f"{n} slots"

def send_message(available_slots):
    text = '*** NEW SLOTS AVAILABLE! ***'

    # format slot info as [weekday, time, count]. Sort it by weekday and time
    sorted_slots = sorted([[(dt := datetime.fromisoformat(x[0])).weekday(), dt.hour, x[1]] for x in available_slots.items()])

    for [weekday, time, count] in sorted_slots:
        text += f"\n{_format_n_slots_(count)} available at {time} on {_format_day_(weekday)}"

    requests.post(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data={ 'chat_id': chat_id, 'text': text }
    )

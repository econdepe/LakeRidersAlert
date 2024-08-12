# WAKE ALERT


## DESCRIPTION

This is a Python script that scrapes the website of LakeRiders Geneva to search for available spots for a wakeboard session. It alerts the user of available sessions through a Telegram bot

## LOGIC

* The script scrapes the calendar of upcoming sessions in the current week in the website every 2 minutes.
* It compares the reserved sessions with the ones from the previous session, which are stored in a LiteSQL DB.
* In case a session has become available (because of cancellation by a member), the script sends a message to a Telegram private group through a Telegram bot.
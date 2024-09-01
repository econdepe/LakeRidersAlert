import os

POLLING_INTERVAL = 120.0
CANCELLED = "CANCELLED"
FREE = "FREE"
EMPTY = "EMPTY"
DB_NAME = "wake_alert.db"

RUN_WITH_LOGS = bool(os.environ.get("RUN_WITH_LOGS"))

# Secrets
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
LOGIN_EMAIL = os.environ.get("LOGIN_EMAIL")
LOGIN_PASSWORD = os.environ.get("LOGIN_PASSWORD")

map = {
    0: "BOT_TOKEN",
    1: "CHAT_ID",
    2: "LOGIN_EMAIL",
    3: "LOGIN_PASSWORD",
}
non_initialized_secrets = ", ".join(
    [
        map[i]
        for i, s in enumerate([BOT_TOKEN, CHAT_ID, LOGIN_EMAIL, LOGIN_PASSWORD])
        if s is None
    ]
)

if non_initialized_secrets:
    raise Exception(
        f"You have not initialized the required secrets {non_initialized_secrets}"
    )

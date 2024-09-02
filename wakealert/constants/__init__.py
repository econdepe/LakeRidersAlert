import os

POLLING_INTERVAL = 120.0
CANCELLED = "CANCELLED"
FREE = "FREE"
EMPTY = "EMPTY"
DB_NAME = "wake_alert.db"

RUN_WITH_LOGS = bool(os.environ.get("RUN_WITH_LOGS"))

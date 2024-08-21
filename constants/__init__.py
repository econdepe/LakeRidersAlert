import os
import sqlite3

POLLING_INTERVAL = 120.0
CANCELLED = 'CANCELLED'
FREE = 'FREE'
DB_NAME = 'wake_alert.db'

# Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
LOGIN_EMAIL = os.environ.get('LOGIN_EMAIL')
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD')

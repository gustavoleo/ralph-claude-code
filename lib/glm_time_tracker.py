import sqlite3
import sys
from datetime import datetime, timedelta, timezone

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False

BEIJING_OFFSET = timedelta(hours=8)

class TimeTracker:
    def __init__(self, db_path="data/glm_queue.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usage_stats
                     (date_str TEXT PRIMARY KEY, requests_sent INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    def _get_beijing_date(self):
        now = datetime.now(timezone.utc)
        if HAS_PYTZ:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            beijing_now = now.astimezone(beijing_tz)
        else:
            beijing_now = now + BEIJING_OFFSET
        return beijing_now.strftime('%Y-%m-%d'), beijing_now

    def get_seconds_until_reset(self):
        date_str, beijing_now = self._get_beijing_date()
        tomorrow_beijing = (beijing_now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        if HAS_PYTZ:
            utc_reset = tomorrow_beijing.astimezone(timezone.utc)
        else:
            utc_reset = tomorrow_beijing - BEIJING_OFFSET
        delta = utc_reset - datetime.now(timezone.utc)
        return max(0, int(delta.total_seconds()))

    def check_and_reset_counters(self):
        current_date, _ = self._get_beijing_date()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT date_str FROM usage_stats WHERE date_str = ?", (current_date,))
        if not c.fetchone():
            c.execute("DELETE FROM usage_stats")
            c.execute("INSERT INTO usage_stats (date_str, requests_sent) VALUES (?, 0)", (current_date,))
            conn.commit()
        conn.close()

    def increment_usage(self):
        current_date, _ = self._get_beijing_date()
        self.check_and_reset_counters()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE usage_stats SET requests_sent = requests_sent + 1 WHERE date_str = ?", (current_date,))
        conn.commit()
        conn.close()

    def get_usage(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT requests_sent FROM usage_stats ORDER BY date_str DESC LIMIT 1")
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0

if __name__ == "__main__":
    tracker = TimeTracker()
    command = sys.argv[1] if len(sys.argv) > 1 else "status"
    if command == "status":
        print(f"{tracker.get_usage()}|{tracker.get_seconds_until_reset()}")
    elif command == "increment":
        tracker.increment_usage()

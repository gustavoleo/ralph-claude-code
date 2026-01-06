import sqlite3
import sys

DB_PATH = "data/glm_queue.db"

def enqueue_request(payload, priority=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO request_queue (payload, priority, status) VALUES (?, ?, 'pending')''', (payload, priority))
    conn.commit()
    conn.close()
    return 0

if __name__ == "__main__":
    payload = sys.argv[1]
    priority = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    sys.exit(enqueue_request(payload, priority))

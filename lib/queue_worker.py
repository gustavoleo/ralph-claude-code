import sqlite3
import asyncio
import time

DB_PATH = "data/glm_queue.db"
MIN_INTERVAL_SEC = 0.5

class QueueWorker:
    def __init__(self):
        self.db_path = DB_PATH
        self.last_request_time = 0
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS request_queue
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT, priority INTEGER DEFAULT 5, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    async def send_request(self, payload):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        wait_time = MIN_INTERVAL_SEC - elapsed
        if wait_time > 0:
            await asyncio.sleep(wait_time)
        await asyncio.sleep(0.2)
        self.last_request_time = time.time()
        return {"status": "success", "data": "GLM Analysis Complete"}

    async def worker_loop(self):
        print("[QueueWorker] Starting...")
        while True:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''SELECT id, payload FROM request_queue WHERE status = 'pending' ORDER BY priority DESC, created_at ASC LIMIT 1''')
            item = c.fetchone()
            if item:
                req_id, payload = item
                c.execute("UPDATE request_queue SET status = 'processing' WHERE id = ?", (req_id,))
                conn.commit()
                conn.close()
                try:
                    await self.send_request(payload)
                    conn = sqlite3.connect(self.db_path)
                    c = conn.cursor()
                    c.execute("UPDATE request_queue SET status = 'done' WHERE id = ?", (req_id,))
                    conn.commit()
                except Exception as e:
                    print(f"Error: {e}")
            else:
                conn.close()
                await asyncio.sleep(0.5)

async def main():
    worker = QueueWorker()
    await worker.worker_loop()

if __name__ == "__main__":
    asyncio.run(main())

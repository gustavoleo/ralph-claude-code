#!/bin/bash
echo ">>> Testing GLM Integration..."
python3 lib/queue_worker.py &
sleep 1
kill %1 2>/dev/null

python3 lib/governor.py "Test Task" 5
COUNT=$(sqlite3 data/glm_queue.db "SELECT COUNT(*) FROM request_queue WHERE status='pending'")

if [ "$COUNT" -eq 1 ]; then
    echo "PASSED: Persistence works."
else
    echo "FAILED: DB issue."
fi

#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

start_worker() {
    python3 $SCRIPT_DIR/lib/queue_worker.py &
    WORKER_PID=$!
    echo $WORKER_PID > .glm_worker_pid
}

stop_worker() {
    if [ -f .glm_worker_pid ]; then
        kill $(cat .glm_worker_pid) 2>/dev/null; rm .glm_worker_pid
    fi
}

trap stop_worker EXIT

start_worker
sleep 1

echo "[Ralph GLM] Loop Running..."
python3 $SCRIPT_DIR/lib/glm_time_tracker.py increment
python3 $SCRIPT_DIR/lib/governor.py "Test Analysis Task" 5
sleep 5
stop_worker

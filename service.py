import zmq
import json
import os
from datetime import datetime

PORT = 5557
LOG_FILE = "history_store.json"
DEFAULT_LIMIT = 5
MAX_LIMIT = 100

# initialize ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{PORT}")

def get_all_logs():
    # helper to load logs from JSON file
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_all_logs(logs):
    # Helper to save logs to JSON file
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

print(f"History Log Service is running on port {PORT}...")

while True:
    # receive the request
    request = socket.recv_json()
    action = request.get("action")

    # handle log action
    if action == "log":
        message_text = request.get("message")
        if message_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message_text}"

            current_logs = get_all_logs()
            current_logs.append(log_entry)
            save_all_logs(current_logs)

            socket.send_json({"status": "success"})
            print(f"Stored log: {log_entry}")
        else:
            socket.send_json({"status": "error", "message": "No message provided"})

    # handle retrieve action
    elif action == "retrieve":
        # get the requested limit, default to 5 otherwise
        requested_limit = request.get("limit", DEFAULT_LIMIT)

        # safety cap - don't allow more than 100 logs at once
        actual_limit = min(max(0, requested_limit), MAX_LIMIT)

        current_logs = get_all_logs()

        # slice list to get the most recent entries
        recent_logs = current_logs[-actual_limit:] if actual_limit > 0 else []

        socket.send_json({
            "status": "success",
            "logs": recent_logs,
            "count": len(recent_logs)
        })
        print(f"Retrieved {len(recent_logs)} logs for client")

    else:
        socket.send_json({"status": "error", "message": "Invalid action"})
import zmq
import json

# set up ZeroMQ client
context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ = request client
socket.connect("tcp://localhost:5557")

print("test.py attempting to connect to History Log server on port 5557...")

# test 1 - log new event
log_data = {
    "action": "log",
    "message": "User connected to microservice."
}

print("\n1. Sending a standard 'log' request...")
socket.send_json(log_data)

log_response = socket.recv_json()
print(f"Server Response: {log_response}")


# test 2 - retrieve with limit
retrieve_data = {
    "action": "retrieve",
    "limit": 3  # asks for just the 3 most recent logs
}

print("\n2. Sending a 'retrieve' request with a limit of 3...")
socket.send_json(retrieve_data)

retrieve_response = socket.recv_json()
print(f"Server Response Status: {retrieve_response['status']}")

if retrieve_response["status"] == "success":
    print(f"Total logs returned: {retrieve_response['count']}")
    print("Logs:")
    for entry in retrieve_response["logs"]:
        print(f"  - {entry}")
else:
    print(f"Error: {retrieve_response.get('message')}")
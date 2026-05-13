# History Log Microservice 

## Description 
This microservice manages a log of user activity and system events.
It allows others services to record timestamped messages and retrieve the recent 
	history for display 

## Communication Contract 

### How to REQUEST data 
Requests are made through ZeroMQ REQ socket 
* PORT: 5557
* FORMAT: JSON Object 

** Example Request ** 
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")

# to log a new activity 
socket.send_json({"action": "log", "messgae": "User 'name' updated their profile"})

### How to RECEIVE data 
The service responds with a JSON object with logs returned in a list 

** Example Request **
socket.send_json({"action": "retrieve", "limit": 5})
response = socket.recv_json()

if response["status"] == "success":
    for entry in response["logs"]:
        print(f"Past Activity: {entry}")

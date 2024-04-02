import socket
import json

BOARDCAST = "0.0.0.0"
PORT = 1111

def receive_msg():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((BOARDCAST, PORT))
        print("Listening")
        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            print("Received broadcast message from {0} : {1}".format(addr, message))
    except Exception as e:
        print("Error receiving broadcast message")


receive_msg()
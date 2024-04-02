import socket
import json
import datetime

BROADCAST = '255.255.255.255'
PORT = 1111

def send_message(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = json.dumps(msg).encode()
        s.sendto(data, (BROADCAST, PORT))
        print("successfully sent")
    except Exception as e:
        print("Error while sending msg:", e)



while True:
    print("", end="\n\n\n\n")
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warning = input("Type of fans warning: ")
    location = input("Location: ")
    description = input("Description: ")

    message = {
        "Date_Time": date_time,
        "Type": warning,
        "Location": location,
        "Description": description
    }

    send_message(message)
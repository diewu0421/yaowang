import time

import socketio
import sys
from socketio.exceptions import ConnectionError
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
client = socketio.Client(logger=True)

if len(sys.argv) < 2:
    raise ValueError("少于两个参数")


@client.on("my_event")
def my_message(data):
    print("my_message", data)


@client.on("message", namespace="/zenglw")
def handle_message(data):
    print("handle_message, ", data)



@client.on("connect", namespace="/zenglw")
def on_connect():
    print("connect " ,  client.sid)


@client.on("disconnect", namespace="/zenglw")
def on_disconnect():
    print("disconnect ", client.sid)


# import time
# time.sleep(3)
# client.emit("leave", {
#     "username": "zenglw",
#     "room": "chat_1"
# })

def send_to_server():
    print("process start---------- ")
    while True:
        str = input("---->")
        if str == "break":
            break
        client.send(str ,namespace="/zenglw")


def get_auth():
    return {
        "sid": client.sid,
        "nversion": 1,
    }

import json
if __name__ == '__main__':

    # with ThreadPoolExecutor() as pp:
    #     time.sleep(3)
    #     pp.submit(send_to_server)

    auth1 = {
            "version": "2",
            "sid": "241"
        }

    print("sid ", client.sid)
    try:

        client.connect("http://127.0.0.1", auth=auth1, namespaces="/zenglw")
        client.emit("join", {
            "username": sys.argv[1],
            "room": sys.argv[2]
        }, namespace="/zenglw")
        time.sleep(1000)
        client.disconnect()
    except ConnectionError as e:
        print("exception ", str(e.args))

    print("he11111111111")

    # client.emit("zenglw_socket", "asdfas")
    # client.emit("message",
    #     {"code": 1, "message": "success", "userId": "10", "approvalId": "10"}
    # , namespace="/zenglw")

    # client.wait()
    # print("11111111")


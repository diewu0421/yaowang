from flask import Flask, request, jsonify, signals
from model import *
from flask_socketio import SocketIO, emit, send, SocketIOTestClient, join_room, leave_room, rooms
from gevent import pywsgi
from engineio.payload import Payload
from configs import DevConfig

Payload.max_decode_packets = 500
app = Flask(__name__)
db_uri = "mysql+pymysql://root:buzhidao@{ipaddress}:{port}/{database}".format(ipaddress="", port="3306",
                                                                              database="sql_test")
print(db_uri)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
# app.config["SQLALCHEMY_ECHO"]= True
app.config["SECRET_KEY"] = 'dsjjkhkhjsdkjchkj'
app.config.from_object(DevConfig)

print("back ", app.config["CELERY_BROKER_URL"])

socketio = SocketIO()

socketio.init_app(app)

# 初始化数据库
with app.app_context():

    db.init_app(app)
    db.create_all()


@app.route("/submit_log", methods=["GET", "POST"])
def report_log():
    print("submit_log", request, type(request.json))
    jj = request.json
    print("log is ", jj["message"])
    return {
        "code": 0,
        "data": "提交成功",
        "msg": jj["message"]
    }


# from celery_task.create_celery import make_celery
# celery = make_celery(app)
# from celery_task.create_celery import send_mail
from  celery_task.tasks import send_mail

@app.route("/test_celery", methods=["GET"])
def test_celery():
    print("task_cenerl")

    send_email_task = send_mail.delay("niasdf")
    print("send_email_task", send_email_task)
    # celery.send_task("send_mail")

    return "success"


# 测试
@app.route('/')
def hello_world():
    a1 = Author(name = "zenglw", age = 30)
    a2 = Author(name = "xixi", age = 27)

    b1 = Book(title = "阿斯蒂芬")
    b2 = Book(title = "kkj")
    b3 = Book(title = "sdf")
    a1.books.append(b1)
    a1.books.append(b3)
    b2.authors.append(a2)
    b3.authors.append(a2)
    db.session.add_all([a1, a2, b1, b2,b3])
    db.session.commit()
    return "success"


@app.route("/getMessage", methods=["GET"])
def getMessage():
    limit = request.args['limit']
    print("requests arg", limit)
    out = ""
    all = list(map(lambda item: str(item), Message.query.limit(limit).all()))
    ret = "\n".join(all)
    print("zenglw_all ", ret)

    return {
        "code": 0,
        "data": ret,
        "msg": ""
    }


from concurrent.futures import ProcessPoolExecutor

import time


def send_test():
    pass


@socketio.on("join", namespace="/zenglw")
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(f"{username} has entered the {room} sid={request.sid},{rooms()}")
    send(f"{username} has entered the {room}.", to=room)


@socketio.on("leave", namespace="/zenglw")
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(f"{username} has left the {room}.${rooms()}")
    send(f"{username} has left the {room}.", to=room)


@socketio.on("zenglw_socket")
def handle_my_custom_event(json):
    print("handle_my_custom_event", json)
    # i = 0
    # with ProcessPoolExecutor() as pp:
    #     pp.submit(send_test)
    send("hello world")

    # i = 0
    # while True:
    #     time.sleep(1)
    #     i = i+1
    #     print("i = ", i)
    #     emit("my_event", "i = %d" % i)
    #     print("emit over")


@socketio.on("message", namespace="/zenglw")
def handle_message(data):
    print("handle_messasge", data)
    msg = Message()
    msg.content = data
    db.session.add(msg)
    db.session.commit()


@socketio.on("connect", namespace='/zenglw')
def on_connect(auth):
    if int(auth["version"]) >= 3:
        raise ConnectionRefusedError("版本太高了兄弟")
    print("connect 111111111", auth, type(auth), "cur items ", socketio.server.eio.sockets)
    # emit('connect', {'data': 'Connected'}, namespace="/zenglw")
    print("给客户端发送消息")
    # await socketio.emit('message', 'calling control', broadcast=False, namespace='/zenglw', room=request.sid)
    emit("message", f"nihao {request.sid}", broadcast=True, room=request.sid)
    print("有新的连接加入：", request.sid)


@socketio.on("disconnect", namespace="/zenglw")
def on_disconnect():
    print("disconnect 11111 ", request.sid)


if __name__ == '__main__':
    # app.run(port="80", host="0.0.0.0")
    socketio.run(app, host="0.0.0.0", port=80)

    # server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    # server.serve_forever()

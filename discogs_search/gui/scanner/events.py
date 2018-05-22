import time
import eventlet
from flask_socketio import send
from .. import socketio


@socketio.on('connected')
def connection_begins(message):
    print('received', message)
    send({'message': 'Hello there!'})


def execution():
    """Simulating long-running task"""
    for i in range(10):
        time.sleep(1)
        yield i


@socketio.on('start')
def handle_message(message):
    print('received', message)
    send({'message': 'Starting here'})
    for i in execution():
        print(i)
        send({'message': i})
        eventlet.sleep(0)
    send({'message': 'Finished here'})
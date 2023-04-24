
from flask_socketio import SocketIO, emit


def clientConnected():
    print('Client connected')


def messageRecieved(message):
    print('Message: ' + message)
    emit('message', message, broadcast=True)

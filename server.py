from flask import Flask, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return 'WebSocket server is running.'

@sock.route('/ws')
def websocket(ws):
    while True:
        data = ws.receive()
        if data:
            print(f'Received: {data}')
            ws.send(f'Echo: {data}')
        else:
            break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

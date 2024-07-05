from flask import Flask, request
from flask_sock import Sock
from main import BusylightController
from termcolor import colored
import datetime
import colorama
import threading
import json
import time


colorama.init()

app = Flask(__name__)
sock = Sock(app)

bs = BusylightController()
last_call_time = datetime.datetime.now()
lock = threading.Lock()

@app.route('/')
def index():
    return 'WebSocket server is running.'

def check_timer():
    while True:
        with lock:
            time_elapsed = datetime.datetime.now() - last_call_time
        if time_elapsed.total_seconds() > 600:  # 10 minutes
            color = bs.parse_color("no call")
            light_resp = bs.send_request("light", color)
            if light_resp.status_code == 200:
                print(colored("Busylight set to busy (red) due to inactivity", "red"))
            else:
                print(f"Error setting light: {light_resp.status_code}")
        time.sleep(60)  # Check every minute

@sock.route('/ws')
def websocket(ws):
    global last_call_time
    while True:
        data = ws.receive()
        if data:
            try:
                json_data = json.loads(data)
                status = json_data.get("status")
                print(f'Received: {status}')
                if status == "call_in_progress":
                    color = bs.parse_color("on call")
                    light_resp = bs.send_request("light", color)
                    if light_resp.status_code == 200:
                        print(colored("Busylight set to on call (green)", "green"))
                        with lock:
                            last_call_time = datetime.datetime.now()
                    else:
                        print(f"Error setting light: {light_resp.status_code}")
                ws.send(json.dumps({"echo": status}))
            except json.JSONDecodeError:
                print("Received non-JSON data")
                ws.send(json.dumps({"error": "Invalid JSON"}))
        else:
            break

if __name__ == '__main__':
    timer_thread = threading.Thread(target=check_timer, daemon=True)
    timer_thread.start()
    app.run(host='0.0.0.0', port=5000)

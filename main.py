import requests
import colorama
from termcolor import colored

class BusylightController:
    COLOR_MAP = {
        "busy": (255, 0, 0),     # Red
        "on call": (0, 255, 0),  # Green
        "away": (255, 255, 0),   # Yellow
        "available": (0, 0, 255) # Blue
        # You can add more states and colors here
    }

    def __init__(self, base_url="http://localhost:8989"):
        self.base_url = base_url

    def send_request(self, action, params):
        url = f"{self.base_url}?action={action}"
        response = requests.get(url, params=params)
        return response

    def parse_color(self, state):
        color = self.COLOR_MAP.get(state.lower())
        if color:
            return {
                "red": color[0],
                "green": color[1],
                "blue": color[2]
            }
        else:
            raise ValueError(f"Invalid state: {state}")

    def play_sound(self, sound_number):
        action = "alert"
        params = {
            "red": 0,
            "sound": sound_number,
            "volume": 75
        }
        response = self.send_request(action, params)
        return response

if __name__ == "__main__":
  
    busylight_controller = BusylightController()

    color = busylight_controller.parse_color("busy")

    response = busylight_controller.send_request("light", color)
    print(response.text)

    if response.status_code == 200:
        print(colored("Busylight set to busy","green"))
    else:
        print(f"Error: {response.status_code}")

    # Example usage: play a sound
    response = busylight_controller.play_sound(3)


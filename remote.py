import os
from flask import Flask, request
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import platform
import subprocess
import socket

app = Flask(__name__)
mouse = MouseController()
keyboard = KeyboardController()

# Yerel IP adresini al
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()

# IP adresini bir dosyaya yaz
with open('ip_address.json', 'w') as f:
    f.write('{"ip_address":"http://'+ip_address+':5005"}' )

@app.route('/mouse_move', methods=['POST'])
def mouse_move():
    current_location = mouse.position
    x = int(request.form.get('x')) + current_location[0]
    y = int(request.form.get('y')) + current_location[1]
    mouse.position = (int(x), int(y))
    print( x, y)
    return "Success", 200

@app.route('/mouse_click', methods=['POST'])
def mouse_click():
    button = request.form.get('button')
    print(button)
    if button == 'left':
        mouse.click(Button.left)
    elif button == 'right':
        mouse.click(Button.right)
    elif button == 'middle':
        mouse.click(Button.middle)
    elif button == 'double':
        mouse.click(Button.left, 2)
    return "Success", 200

@app.route('/keyboard_type', methods=['POST'])
def keyboard_type():
    keys = request.form.get('keys')
    keyboard.type(keys)
    return "Success", 200

@app.route('/press_key', methods=['POST'])
def press_key():
    key = request.form.get('key')
    print(key)
    if key == 'play_pause':
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
    elif key == 'volume_up':
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
    elif key == 'volume_down':
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    elif key == 'next':
        keyboard.press(Key.media_next)
        keyboard.release(Key.media_next)
    elif key == 'previous':
        keyboard.press(Key.media_previous)
        keyboard.release(Key.media_previous)
    elif key == 'mute':
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
    elif key == 'fullscreen':
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)
    elif key == 'stop':
        keyboard.press(Key.stop)
        keyboard.release(Key.stop)
    elif key == 'enter':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif key == 'backspace':
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    elif key == 'esc':
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
    elif key == 'tab':
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif key == 'space':
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif key == 'up':
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif key == 'down':
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif key == 'left':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif key == 'right':
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif key == 'zoom_in':
        keyboard.press(Key.cmd_l)
        keyboard.press('+')
        keyboard.release('+')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('+')
        keyboard.release('+')
        keyboard.release(Key.ctrl_l)
    elif key == 'zoom_out':
        keyboard.press(Key.cmd_l)
        keyboard.press('-')
        keyboard.release('-')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('-')
        keyboard.release('-')
        keyboard.release(Key.ctrl_l)
    elif key == 'refresh':
        keyboard.press(Key.cmd_l)
        keyboard.press('r')
        keyboard.release('r')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    elif key == 'new_tab':
        keyboard.press(Key.cmd_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.ctrl_l)
    elif key == 'close_tab':
        keyboard.press(Key.cmd_l)
        keyboard.press('w')
        keyboard.release('w')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('w')
        keyboard.release('w')
        keyboard.release(Key.ctrl_l)
    elif key == 'google':
        keyboard.press(Key.cmd_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.ctrl_l)
        keyboard.type("https://www.google.com")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif key == 'youtube':
        keyboard.press(Key.cmd_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.ctrl_l)
        keyboard.type("https://www.youtube.com/tv")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif key == 'netflix':
        keyboard.press(Key.cmd_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.cmd_l)
        keyboard.press(Key.ctrl_l)
        keyboard.press('t')
        keyboard.release('t')
        keyboard.release(Key.ctrl_l)
        keyboard.type("https://www.netflix.com")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        
    
    # Add more keys if needed
    return "Success", 200

@app.route('/app_list', methods=['POST'])
def app_list():
    return get_open_applications(), 200
def get_open_applications_windows():
    try:
        from pywinauto import Application
        app = Application().connect()
        return [(proc.process_id(), proc.name()) for proc in app.processes()]
    except ImportError:
        print("pywinauto module is not installed. Install it with 'pip install pywinauto'")
        return []

def get_open_applications_mac():
    output = subprocess.check_output(['osascript', '-e', 'tell application "System Events" to get name of (processes where background only is false)'])
    applist =  output.decode('utf-8').split(', ')
    return [i for i in applist]


def get_open_applications():
    os_name = platform.system()
    if os_name == 'Windows':
        return get_open_applications_windows()
    elif os_name == 'Darwin':
        return get_open_applications_mac()
    else:
        print(f"{os_name} is not supported.")
        return []




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
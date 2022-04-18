from time import sleep
from threading import Event
import pygame.mixer
import os, subprocess, io
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory
import keyboard

print("SpecDeck!")
my_directory = os.path.dirname(os.path.realpath(__file__))
config = {
    "tzx_directory": my_directory + "/tzx/",
    "tzxplay_bin": subprocess.run(['which', 'tzxplay'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip(),
    "tmp_wav": my_directory + "/tmp.wav",
    "cache_wavs": False
}
selected_tzx = 0
is_loaded = False

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

def mock_gpio(gpio):
    gpio.pin.drive_low()
    gpio.pin.drive_high()

def keyboard_p():
    mock_gpio(button_a)

def keyboard_r():
    mock_gpio(button_b)

def keyboard_q():
    mock_gpio(button_x)

def keyboard_w():
    mock_gpio(button_y)

def button_a_press():
    global is_loaded, tzx_files
    if not is_loaded:
        print("Converting " + tzx_files[selected_tzx] + " to WAV")
        tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , config["tmp_wav"], config["tzx_directory"] + "Jetpac.tzx" ]).returncode
        if tzxplay_result is not 0:
            print("Conversion failed: " + tzxplay_result)
            return
        print("Playing " + tzx_files[selected_tzx])
        pygame.mixer.music.load(config["tmp_wav"])
        pygame.mixer.music.play()
        is_loaded = True
    elif pygame.mixer.music.get_busy():
        print("Pausing")
        pygame.mixer.music.pause()
    else:
        print("Unpausing")
        pygame.mixer.music.unpause()
    sleep(0.1)

def button_b_press():
    global is_loaded
    if not is_loaded:
        print("No tzx playing")
    else:
        print("Rewinding and pausing")
        pygame.mixer.music.play(0, 0)
        pygame.mixer.music.pause()
        sleep(0.1)

def change_selection(left):
    global selected_tzx, is_loaded, tzx_files
    if left:
        selected_tzx = len(tzx_files) - 1 if selected_tzx == 0 else selected_tzx - 1
    else:
        selected_tzx =  0 if selected_tzx == len(tzx_files) - 1 else selected_tzx + 1
    print('Selected ' + tzx_files[selected_tzx])
    pygame.mixer.music.unload()
    is_loaded = False

def button_x_press():
    change_selection(True)

def button_y_press():
    change_selection(False)

print("Initialising")
# Allows development on non-Raspberry Pi platforms without GPIO
if is_raspberrypi() is False:
    Device.pin_factory = MockFactory()
    keyboard.add_hotkey('p', keyboard_p)
    keyboard.add_hotkey('r', keyboard_r)
    keyboard.add_hotkey('q', keyboard_q)
    keyboard.add_hotkey('w', keyboard_w)

button_a = Button(5)
button_a.when_pressed = button_a_press
button_b = Button(6)
button_b.when_pressed = button_b_press
button_x = Button(16)
button_x.when_pressed = button_x_press
button_y = Button(24)
button_y.when_pressed = button_y_press

pygame.mixer.init()
pygame.mixer.music.set_volume(1)

# This reads all the files in the directory and returns a list of files ending .tzx without the .tzx extension
tzx_files = [f.rsplit('.', 1)[0] for f in os.listdir(config["tzx_directory"]) if os.path.isfile(os.path.join(config["tzx_directory"], f)) and f.lower().endswith('.tzx')]
tzx_files.sort()
if len(tzx_files) == 0:
    print("No tzx files found!")
    exit()

print("Selected " + tzx_files[selected_tzx])


#print("Converting to WAV")
#tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , config["tmp_wav"], config["tzx_directory"] + "Jetpac.tzx" ]).returncode

#print("Playing WAV")
#pygame.mixer.music.load(config["tmp_wav"])
#pygame.mixer.music.play()

# Wait forever
Event().wait()

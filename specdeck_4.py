from time import sleep
from threading import Event
import pygame.mixer
import os, subprocess, io
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory
import keyboard

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

def button_a_press():
    if pygame.mixer.music.get_busy():
        print("Pausing")
        pygame.mixer.music.pause()
    else:
        print("Unpausing")
        pygame.mixer.music.unpause()
    sleep(0.1)

def button_b_press():
    print("Rewinding and pausing")
    pygame.mixer.music.play(0, 0)
    pygame.mixer.music.pause()
    sleep(0.1)

print("SpecDeck!")
my_directory = os.path.dirname(os.path.realpath(__file__))
config = {
    "tapes_directory": my_directory + "/tapes/",
    "tzxplay_bin": subprocess.run(['which', 'tzxplay'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip(),
    "tmp_wav": my_directory + "/tmp.wav",
    "cache_wavs": False
}

print("Initialising")
# Allows development on non-Raspberry Pi platforms without GPIO
if is_raspberrypi() is False:
    Device.pin_factory = MockFactory()
    keyboard.add_hotkey('p', keyboard_p)
    keyboard.add_hotkey('r', keyboard_r)

button_a = Button(5)
button_a.when_pressed = button_a_press
button_b = Button(6)
button_b.when_pressed = button_b_press

pygame.mixer.init()
pygame.mixer.music.set_volume(1)

print("Converting to WAV")
tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , config["tmp_wav"], config["tapes_directory"] + "Jetpac.tzx" ]).returncode

print("Playing WAV")
pygame.mixer.music.load(config["tmp_wav"])
pygame.mixer.music.play()

# Wait forever
Event().wait()

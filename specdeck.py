from time import sleep
import pygame.mixer
import os, subprocess
import keyboard
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory

print("SpecDeck!")
my_directory = os.path.dirname(os.path.realpath(__file__))
config = {
    "tapes_directory": my_directory + "/tapes/",
    "tzxplay_bin": subprocess.run(['which', 'tzxplay'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip(),
    "tmp_wav": my_directory + "/tmp.wav",
    "cache_wavs": False
}

print("Initialising")
# Allows development on non-Raspberry Pi platforms
if Device.pin_factory is None:
    Device.pin_factory = MockFactory()
button_a = Button(5)
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

print("Converting to WAV")
tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , config["tmp_wav"], config["tapes_directory"] + "Jetpac.tzx" ]).returncode

print("Playing WAV")
pygame.mixer.music.load(config["tmp_wav"])
pygame.mixer.music.play()

# Main event loop
while True:
    if button_a.is_pressed or keyboard.read_key() == 'p':
        if pygame.mixer.music.get_busy():
            print("Pausing")
            pygame.mixer.music.pause()
        else:
            print("Unpausing")
            pygame.mixer.music.unpause()
    sleep(0.1)

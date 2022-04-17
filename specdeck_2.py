from time import sleep
import pygame.mixer
import os, subprocess

print("SpecDeck!")
my_directory = os.path.dirname(os.path.realpath(__file__))
config = {
    "tapes_directory": my_directory + "/tapes/",
    "tzxplay_bin": subprocess.run(['which', 'tzxplay'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip(),
    "tmp_wav": my_directory + "/tmp.wav",
    "cache_wavs": False
}

print("Initialising")
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

print("Converting to WAV")
tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , config["tmp_wav"], config["tapes_directory"] + "Jetpac.tzx" ]).returncode

print("Playing WAV")
pygame.mixer.music.load(config["tmp_wav"])
pygame.mixer.music.play()
while True:
    sleep(0.1)

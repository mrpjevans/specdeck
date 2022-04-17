from time import sleep
import pygame.mixer
pygame.mixer.init()
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load("tapes/Jetpac.wav")
pygame.mixer.music.play()
while True:
    sleep(0.1)

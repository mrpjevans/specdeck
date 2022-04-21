import os, subprocess, io
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from time import sleep
from threading import Event
import pygame.mixer
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory
import keyboard

try:
    with io.open("/sys/firmware/devicetree/base/model", "r") as m:
        is_raspberrypi = True if "raspberry pi" in m.read().lower() else False
except Exception:
    is_raspberrypi = False

if is_raspberrypi:
    import display

print("SpecDeck!")
my_directory = os.path.dirname(os.path.realpath(__file__))
config = {
    "tzx_directory": my_directory + "/tzx/",
    "wav_directory": my_directory + "/wav/",
    "img_directory": my_directory + "/image/",
    "tzxplay_bin": subprocess.run(['which', 'tzxplay'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip(),
    "tmp_wav": my_directory + "/tmp.wav",
    "cache_wavs": True
}
if os.path.isfile(my_directory + "/config.py"):
    import config as override_config
    config = config | override_config.config

selected_tzx = -1
is_loaded = False

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

def convert_and_play():
    global tzx_files, selected_tzx, is_loaded, config, is_raspberrypi
    play_wav = config["wav_directory"] + tzx_files[selected_tzx] + ".wav"
    # Is there a cached WAV? If not, convert.
    if not os.path.isfile(play_wav):
        if config["cache_wavs"] is False: play_wav = config["tmp_wav"]
        print("Converting " + tzx_files[selected_tzx])
        if is_raspberrypi:
            display.display_text("Converting")
        tzxplay_result = subprocess.run([config["tzxplay_bin"], "-o" , play_wav, config["tzx_directory"] + tzx_files[selected_tzx] + ".tzx" ]).returncode
        if is_raspberrypi:
            display.display(config["img_directory"] + tzx_files[selected_tzx] + ".jpg", tzx_files[selected_tzx])
        if tzxplay_result != 0:
            print(config["tzx_directory"] + tzx_files[selected_tzx])
            print("Conversion failed: " + str(tzxplay_result))
            if is_raspberrypi:
                display.display_text("Failed! :(")
            return
    print("Playing " + tzx_files[selected_tzx])
    pygame.mixer.music.load(play_wav)
    pygame.mixer.music.play()
    is_loaded = True

def button_a_press():
    global is_loaded, tzx_files
    if not is_loaded:
        convert_and_play()
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

def button_b_when_held():
    print("Shutdown")
    if is_raspberrypi:
        display.display_text("Shutdown")
    subprocess.run("sudo shutdown -h now", shell=True)


def change_selection(up):
    global selected_tzx, is_loaded, tzx_files
    if up:
        selected_tzx = len(tzx_files) - 1 if selected_tzx == 0 else selected_tzx - 1
    else:
        selected_tzx = 0 if selected_tzx == len(tzx_files) - 1 else selected_tzx + 1
    print('Selected ' + tzx_files[selected_tzx])
    if is_raspberrypi:
        display.display(config["img_directory"] + tzx_files[selected_tzx] + ".jpg", tzx_files[selected_tzx])
    pygame.mixer.music.unload()
    is_loaded = False

def button_x_press():
    change_selection(True)

def button_y_press():
    change_selection(False)

print("Initialising")
# Allows development on non-Raspberry Pi platforms without GPIO
if is_raspberrypi is False:
    Device.pin_factory = MockFactory()
    keyboard.add_hotkey('p', keyboard_p)
    keyboard.add_hotkey('r', keyboard_r)
    keyboard.add_hotkey('q', keyboard_q)
    keyboard.add_hotkey('w', keyboard_w)
else:
    display.init()
    display.display_text("SpecDeck!")
    sleep(1)

button_a = Button(5)
button_a.when_pressed = button_a_press
button_b = Button(6, hold_time = 5)
button_b.when_pressed = button_b_press
button_b.when_held = button_b_when_held
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

change_selection(False)
if is_raspberrypi:
    display.display(config["img_directory"] + tzx_files[selected_tzx] + ".jpg", tzx_files[selected_tzx])

# Wait forever
Event().wait()

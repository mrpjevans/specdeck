# SpecDeck
Load game and programs to your ZX Spectrum directly from a Raspberry Pi.

## Features
- TZX and WAV Support
- Cover display on Pirate Audio screen
- Select, playback, rewind and shutdown from Pirate Audio controls

## You Will Need
- Raspberry Pi Zero WH (with GPIO header)
- Pimoroni Pirate Audio Headphone Amp HAT
- Additional headphone amplifier (see notes)

## Installation

Before installing, make sure you have physically installed the Pirate Audio HAT and added the following to `/boot/config.txt`:

```
dtoverlay=hifiberry-dac
gpio=25=op,dh
dtparam=audio=off
```

Reboot, then add the dependancies:

```bash
sudo apt -y update && sudo apt -y upgrade
sudo apt install git libsdl2-mixer-2.0-0 python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy libatlas-base-dev libportaudio2python3-pip python3-pil python3-numpy
sudo pip3 install pygame keyboard st7789 tzxtools
```

Now you can clone this repo:
```bash
cd
git clone https://github.com/mrpjevans/specdeck.git
```

Everything is now in `~/specdeck`

## Running
To run manually:

```bash
cd ~/specdeck
sudo python3 specdeck.py
```
 
To run as service on startup:

```bash
sudo nano /usr/lib/systemd/specdeck.service
```

Add the following:

```
[Unit]
Description=specdeck

[Service]
ExecStart=/usr/bin/python3 /home/pi/specdeck/specdeck.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

(Provided in specdeck.service)

Save and close, then enable:

```
sudo systemctl enable /usr/lib/systemd/specdeck.service
```

Test by rebooting:

```
sudo reboot
```


## Adding Games
Place TZX files in the `tzx` folder. These will be converted on first run to WAV and then cached in the `wav` folder so subsequent playbacks will be instantaneous. 

## Cover Art
When selecting a file, by default the filename is displayed on screen. However, if an identifically named `.jpg` file is found in the `image` directory, this will be resized to fit and displayed instead.

e.g. If we have
```
tzx/Hungry Horace.tzx
```
Then you would set the image to be
```
image/Hungry Horace.jpg
```
and this image will be picked up automatically.

## Using SpecDeck
Once loaded, the first game will be displayed. You ca then use the following controls on the Pirate Audio HAT:

A: Play/Pause

B: Rewind and pause

X: Previous file

Y: Next file

To shutdown cleanly, press and hold B for at least 5 seconds.

## Acknowledgments

- ZX Spectrum TTF Font: http://www.styleseven.com/
- Raspberry Pi logo conversion made with: http://www.fruitcake.plus.com/Sinclair/Spectrum/Spectra/SpectraInterface_Software_ImageConverter.htm

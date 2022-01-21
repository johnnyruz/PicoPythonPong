# PicoPythonPong

This is a sample application that came about based on impulse buying at MicroCenter!

I picked up a couple Raspberry Pi Pico boards along with a Pimoroni Pico Display and a Pico Decker development board. I wanted to create something cool and learn a little bit about MicroPython development.

Certainly not flawless code, but if you have a Pico with a Pico Display this code should run well and show off some of the capabilies of the display.

## Setup
1. Connect in bootloader mode and flash Pimoroni's custom MicroPython FW (Available at their GitHub Repo [HERE](https://github.com/pimoroni/pimoroni-pico/releases))
2. Connect to your Pico using something like Thonny. I personally use Visual Studio Code with the Pico-Go Extension
3. Upload the `pong.py` file to your Pico
4. Run the program

## Run on startup

If you want to run the application as soon as your Pico starts up, you can rename the `pong.py` file to `main.py` and upload to your device

**NOTE:** if you do this you will lose the ability to connect to your device and upload files. You will need to wipe your Pico by connecting in bootloader mode and uploading a "Nuke" file to wipe the flash (search for flash_nuke.uf2). You will then have to reload the MicroPython firmware from step 1.

## Game Options

- 1 player or 2 player mode
- Use X and Y buttons on the Pico Display to make menu selection
- Press the A button to start the game
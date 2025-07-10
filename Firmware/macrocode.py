import RPi.GPIO as GPIO
from pynput.keyboard import Controller, Key
import time

# Setup keyboard controller
keyboard = Controller()

# GPIO pin mapping for each button
BUTTON_PINS = {
    1: 5,
    2: 6,
    3: 13,
    4: 19,
    5: 26,
    6: 21
}

# Define the function of each button (key combinations)
BUTTON_ACTIONS = {
    1: [Key.ctrl, 'c'],   # Copy
    2: [Key.ctrl, 'v'],   # Paste
    3: [Key.ctrl, 'z'],   # Undo
    4: [Key.ctrl, 'y'],   # Redo
    5: [Key.ctrl, 's'],   # Save
    6: [Key.alt, Key.tab] # Alt+Tab (task switch)
}

# Setup GPIO
GPIO.setmode(GPIO.BCM)

for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def press_shortcut(keys):
    for key in keys:
        keyboard.press(key)
    for key in reversed(keys):
        keyboard.release(key)

def button_callback(channel):
    for btn_num, pin in BUTTON_PINS.items():
        if channel == pin:
            print(f"Button {btn_num} pressed")
            press_shortcut(BUTTON_ACTIONS[btn_num])
            break

# Add event detection
for pin in BUTTON_PINS.values():
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=300)

try:
    print("MacroPad is running. Press Ctrl+C to exit.")
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
"""
move_hand.py

Manual testing for moving one clock hand to a saved position.

This script:
1. Loads servo positions from clock_positions.json
2. Lets you select a person/hand
3. Lets you select a clock location
4. Sends the saved duty-cycle value to the corresponding PCA9685 channel

Hardware:
- Raspberry Pi
- PCA9685 PWM servo driver
- Four independently controlled servos

"""

import json
from pathlib import Path
import board
import busio
from adafruit_pca9685 import PCA9685


# config

# locate the project root regardless of where this script is run
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# users should copy:
# config/clock_positions.example.json
# to:
# config/clock_positions.json
# and replace the example values with their own calibration
POSITIONS_FILE = PROJECT_ROOT / "config" / "clock_positions.json"


# map each clock hand/person to a PCA9685 channel
# change these if your servos are connected to different channels
PERSON_TO_CHANNEL = {
    "person1": 0,
    "person2": 1,
    "person3": 2,
    "person4": 3,
}


# functions

def match_location(user_input, available_locations):
    """
    Match a typed location to one in the calibration file.
    Matching is case-insensitive, so "home", "Home", and "HOME"
    will all match the saved location "Home".
    """

    cleaned_input = user_input.strip().lower()

    for location in available_locations:
        if location.lower() == cleaned_input:
            return location

    return None


# main program

def main():

    if not POSITIONS_FILE.exists():
        print("\nCould not find clock_positions.json.")
        print()
        print("Copy:")
        print("  config/clock_positions.example.json")
        print()
        print("to:")
        print("  config/clock_positions.json")
        print()
        print("Then calibrate your clock before running this script.")
        return

    # load saved servo positions
    with open(POSITIONS_FILE, "r") as file:
        positions = json.load(file)

    print("\nAvailable clock hands:")

    for person, channel in PERSON_TO_CHANNEL.items():
        print(f"- {person.title()} — PCA9685 channel {channel}")

    # loop for peron selection

    while True:

        person = input("\nSelect a clock hand, or type q to quit: ").strip().lower()

        if person == "q":
            return

        if person not in PERSON_TO_CHANNEL:
            print("Unknown clock hand.")
            continue

        if person not in positions:
            print(f"No calibration data exists for '{person}'.")
            continue

        channel = PERSON_TO_CHANNEL[person]
        available_locations = list(positions[person].keys())

        # initialize PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        pca = PCA9685(i2c)

        # servos used in this project are controlled at 50 Hz
        pca.frequency = 50

        print(f"\nControlling {person.title()} "f"on PCA9685 channel {channel}.")
        print("\nAvailable locations:")

        for location in available_locations:

            saved_value = positions[person][location]

            if saved_value is None:
                print(f"- {location} — not calibrated")
            else:
                print(f"- {location}")

        print("\nCommands:")
        print("Enter a location name to move the hand.")
        print("Type 'person' to select another clock hand.")
        print("Type 'q' to quit.")

        # loop for location selection

        try:

            while True:

                user_input = input(f"\n{person.title()} location: ").strip()

                if user_input.lower() == "q":
                    return

                if user_input.lower() == "person":
                    break

                location = match_location(user_input,available_locations)

                if location is None:
                    print("Unknown location.")
                    continue

                value = positions[person].get(location)

                if value is None:
                    print(f"{person.title()} has not been "f"calibrated for {location}.")
                    continue

                print(f"Moving {person.title()} → {location} "f"(channel {channel}, duty cycle {value})")

                # send the calibrated dutycycle value directly to selected PCA channel
                pca.channels[channel].duty_cycle = int(value)

        finally:

            # close the PCA9685 connection before selecting another hand or exting
            pca.deinit()


if __name__ == "__main__":
    main()

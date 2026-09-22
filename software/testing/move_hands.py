"""manual utility for moving multiple clock hands to saved positions"""

import json
from pathlib import Path
import board
import busio
from adafruit_pca9685 import PCA9685

# configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]
POSITIONS_FILE = PROJECT_ROOT / "config" / "clock_positions.json"

# map each clock hand to its pca9685 channel
PERSON_TO_CHANNEL = {
    "person1": 0,
    "person2": 1,
    "person3": 2,
    "person4": 3,
}

def match_location(user_input, available_locations):
    """match typed location to saved location"""
    cleaned_input = user_input.strip().lower()
    for location in available_locations:
        if location.lower() == cleaned_input:
            return location
    return None

def move_hand(pca, positions, person, location):
    """move one hand to a saved location"""
    if person not in PERSON_TO_CHANNEL:
        print(f"unknown clock hand: {person}")
        return
    if person not in positions:
        print(f"no calibration data exists for {person}")
        return

    matched_location = match_location(location, positions[person].keys())
    if matched_location is None:
        print(f"unknown location for {person}: {location}")
        return

    value = positions[person].get(matched_location)
    if value is None:
        print(f"{person} has not been calibrated for {matched_location}")
        return

    channel = PERSON_TO_CHANNEL[person]
    print(f"moving {person} → {matched_location} | channel {channel} | duty cycle {value}")
    pca.channels[channel].duty_cycle = int(value)

def main():
    # check for calibration file
    if not POSITIONS_FILE.exists():
        print("\ncould not find clock_positions.json")
        print("copy config/clock_positions.example.json to config/clock_positions.json")
        print("then calibrate your clock before running this script")
        return

    # load saved positions
    with open(POSITIONS_FILE, "r") as file:
        positions = json.load(file)

    # initialize pca9685
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50

    print("\navailable clock hands:")
    for person, channel in PERSON_TO_CHANNEL.items():
        print(f"- {person} — channel {channel}")

    print("\nenter commands as person, location")
    print("example: person1, Home")
    print("type all to move every hand")
    print("type q to quit")

    try:
        while True:
            command = input("\ncommand: ").strip()
            if command.lower() == "q":
                break

            if command.lower() == "all":
                location = input("location for all hands: ").strip()
                for person in PERSON_TO_CHANNEL:
                    move_hand(pca, positions, person, location)
                continue

            if "," not in command:
                print("use format: person1, Home")
                continue

            person, location = [part.strip() for part in command.split(",", 1)]
            person = person.lower()
            move_hand(pca, positions, person, location)
    finally:
        pca.deinit()

if __name__ == "__main__":
    main()

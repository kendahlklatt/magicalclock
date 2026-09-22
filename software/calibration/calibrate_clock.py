"""interactive utility for calibrating clock hand positions"""

import json
from pathlib import Path
import board
import busio
from adafruit_pca9685 import PCA9685

# configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]
POSITIONS_FILE = PROJECT_ROOT / "config" / "clock_positions.json"
PERSON_TO_CHANNEL = {
    "person1": 0,
    "person2": 1,
    "person3": 2,
    "person4": 3,
}
LOCATIONS = ["Home", "Work", "5346", "Mortal Peril", "In Transit", "Adventure"]
START_VALUE = 4500
MIN_VALUE = 0
MAX_VALUE = 65535

def load_positions():
    """load existing calibration or create a blank one"""
    if POSITIONS_FILE.exists():
        with open(POSITIONS_FILE, "r") as file:
            return json.load(file)
    return {person: {location: None for location in LOCATIONS} for person in PERSON_TO_CHANNEL}

def save_positions(positions):
    """save calibration values"""
    POSITIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POSITIONS_FILE, "w") as file:
        json.dump(positions, file, indent=2)

def main():
    positions = load_positions()
    print("\navailable clock hands:")
    for person, channel in PERSON_TO_CHANNEL.items():
        print(f"- {person} — channel {channel}")

    person = input("\nselect clock hand: ").strip().lower()
    if person not in PERSON_TO_CHANNEL:
        print("unknown clock hand")
        return

    print("\navailable locations:")
    for location in LOCATIONS:
        print(f"- {location}")

    location_input = input("\nselect location: ").strip().lower()
    location = next((x for x in LOCATIONS if x.lower() == location_input), None)
    if location is None:
        print("unknown location")
        return

    channel = PERSON_TO_CHANNEL[person]
    saved_value = positions.get(person, {}).get(location)
    value = int(saved_value) if saved_value is not None else START_VALUE

    # initialize pca9685
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
    pca.channels[channel].duty_cycle = value

    print(f"\ncalibrating {person} → {location}")
    print(f"starting duty cycle: {value}")
    print("\nj/l = -/+ 10")
    print("a/d = -/+ 100")
    print("A/D = -/+ 500")
    print("s = save")
    print("q = quit")

    try:
        while True:
            command = input(f"\n{value} > ")
            if command == "q":
                break
            if command == "s":
                positions.setdefault(person, {})[location] = value
                save_positions(positions)
                print(f"saved {person} → {location} = {value}")
                break

            changes = {"j": -10, "l": 10, "a": -100, "d": 100, "A": -500, "D": 500}
            if command not in changes:
                print("unknown command")
                continue

            value = max(MIN_VALUE, min(MAX_VALUE, value + changes[command]))
            pca.channels[channel].duty_cycle = value
    finally:
        pca.deinit()

if __name__ == "__main__":
    main()

"""receive owntracks locations and move clock hands based on geofences"""

import json
from pathlib import Path
from flask import Flask, request, jsonify
from shapely.geometry import Point, shape
import board
import busio
from adafruit_pca9685 import PCA9685

# configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ZONES_FILE = PROJECT_ROOT / "config" / "zones.geojson"
POSITIONS_FILE = PROJECT_ROOT / "config" / "clock_positions.json"

PERSON_TO_CHANNEL = {
    "person1": 0,
    "person2": 1,
    "person3": 2,
    "person4": 3,
}

ZONE_TO_POSITION = {
    "home": "Home",
    "work": "Work",
    "favorite": "Favorite Place",
}

# initialize flask and pca9685
app = Flask(__name__)
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50
CURRENT_STATE = {}

def load_json(path):
    """load a json file"""
    if not path.exists():
        raise FileNotFoundError(f"missing required file: {path}")
    with open(path, "r") as file:
        return json.load(file)

def load_geofences():
    """load person specific geofences"""
    data = load_json(ZONES_FILE)
    geofences = []
    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        person = str(properties.get("person", "")).strip().lower()
        zone = str(properties.get("zone", "")).strip().lower()
        geometry = feature.get("geometry")
        if person and zone and geometry:
            geofences.append({"person": person, "zone": zone, "geometry": shape(geometry)})
    return geofences

CLOCK_POSITIONS = load_json(POSITIONS_FILE)
GEOFENCES = load_geofences()

def get_zone(person, latitude, longitude):
    """find which saved geofence contains a person"""
    point = Point(longitude, latitude)
    for geofence in GEOFENCES:
        if geofence["person"] != person:
            continue
        if geofence["geometry"].covers(point):
            return geofence["zone"]
    return None

def move_hand(person, position):
    """move a clock hand to a saved position"""
    if person not in PERSON_TO_CHANNEL:
        return False
    value = CLOCK_POSITIONS.get(person, {}).get(position)
    if value is None:
        return False
    if CURRENT_STATE.get(person) == position:
        return True

    channel = PERSON_TO_CHANNEL[person]
    pca.channels[channel].duty_cycle = int(value)
    CURRENT_STATE[person] = position
    print(f"{person} → {position} | channel {channel} | duty cycle {value}")
    return True

def process_location(person, data):
    """process an owntracks location update"""
    if data.get("_type") != "location":
        return {"status": "ignored", "reason": "not a location update"}

    latitude = data.get("lat")
    longitude = data.get("lon")
    if latitude is None or longitude is None:
        return {"status": "ignored", "reason": "missing coordinates"}

    zone = get_zone(person, latitude, longitude)
    if zone is None:
        print(f"{person} → outside saved geofences")
        return {"status": "ok", "person": person, "zone": None, "position": None}

    position = ZONE_TO_POSITION.get(zone)
    if position is None:
        print(f"{person} → unrecognized zone {zone}")
        return {"status": "ok", "person": person, "zone": zone, "position": None}

    moved = move_hand(person, position)
    return {"status": "ok", "person": person, "zone": zone, "position": position, "moved": moved}

@app.route("/owntracks/<person>", methods=["POST"])
def owntracks(person):
    """receive an owntracks update"""
    person = person.strip().lower()
    if person not in PERSON_TO_CHANNEL:
        return jsonify({"status": "error", "message": "unknown person"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "invalid json"}), 400

    return jsonify(process_location(person, data))

@app.route("/", methods=["GET"])
def status():
    """simple server status page"""
    return jsonify({"status": "running", "hands": list(PERSON_TO_CHANNEL.keys())})

if __name__ == "__main__":
    print(f"loaded {len(GEOFENCES)} geofences")
    print("waiting for location updates")
    app.run(host="0.0.0.0", port=5000, threaded=False)

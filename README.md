# location clock
open-source, enchanted location tracking for you and yours

location clock turns phone location data into a physical display
instead of stalking your mom or dad or sibling or friend on an app, look at a clock that moves that persons hand to a designated place!

the current prototype uses a raspberry pi, owntracks, a pca9685 servo controller, four servos, and four independently moving clock hands

> this project is currently under active development and full beginner-friendly build instructions are coming soon!

##  how it works

```text
phone
  ↓
owntracks
  ↓
raspberry pi
  ↓
geofence detection
  ↓
location state
  ↓
pca9685
  ↓
servo
  ↓
clock hand
```
each phone sends location updates to the raspberry pi using owntracks
-> 
the pi checks whether that person is inside one of their saved geofences and converts the result into a clock state such as home or work
->
the corresponding servo then moves that person's hand to the calibrated position on the clock face

##  hardware

the current four-hand prototype uses:

- raspberry pi
- pca9685 16-channel pwm servo driver
- 4 servos
- 4 large driven gears
- 4 smaller servo gears
- concentric telescoping tubing
- 5v servo power supply
- donor clock case
- custom clock hands and face

the four hands rotate independently using a single concentric shaft assembly driven by four separate servos

##  software

the project is organized into three main parts:

```text
software/
├── main/
│   └── owntracks_receiver.py
├── calibration/
│   └── calibrate_clock.py
└── testing/
    ├── move_hand.py
    └── move_hands.py
```

`owntracks_receiver.py` receives location updates, checks geofences, and moves the appropriate hand

`calibrate_clock.py` is used to save the physical servo position for each clock location

`move_hand.py` and `move_hands.py` provide simple manual controls for testing the mechanism

##  configuration

private configuration is stored separately from the main software...

```text
config/
├── zones.example.geojson
└── clock_positions.example.json
```

copy the example files before configuring your own clock...

```bash
cp config/zones.example.geojson config/zones.geojson
cp config/clock_positions.example.json config/clock_positions.json
```

your real configuration files are ignored by git so personal locations and calibration values are not accidentally uploaded to github.

##  basic setup

clone the repository and enter the project folder

```bash
git clone <repository-url>
cd <repository-name>
```

create a python virtual environment

```bash
python3 -m venv clockenv
source clockenv/bin/activate
```

install the required packages

```bash
pip install -r requirements.txt
```

after wiring the electronics, begin by testing one hand

```bash
python software/testing/move_hand.py
```

then calibrate the clock

```bash
python software/calibration/calibrate_clock.py
```

once your geofences and calibration are configured, start the location receiver

```bash
python software/main/owntracks_receiver.py
```

## privacy

this project is designed around meaningful location states rather than continuously displaying someone's exact position on a map!

(real geofence coordinates, calibration files, credentials, and other private configuration should never be committed to a public repository)

the included `.gitignore` helps prevent these files from being uploaded accidentally!

##  clock states

the clock is being developed around six location states

- home
- work
- custom location
- adventure
- in transit
- mortal peril

the current public receiver supports saved geofences such as home, work, and custom locations

(automatic movement and battery-based states are still under development)

## project status

the physical four-hand prototype is working and the software and documentation are currently being prepared for public release

upcoming work includes

- automatic movement detection for in transit
- automatic adventure detection
- battery-based mortal peril
- improved calibration
- mechanical diagrams
- wiring diagrams
- complete assembly instructions
- beginner-friendly documentation

##  documentation

full step-by-step build instructions are coming soon!!!

the goal is to make this project approachable even if you have never used a raspberry pi, worked with servos, configured location tracking, or written python before :) 

the documentation will cover the complete build from modifying the clock and assembling the concentric hand mechanism through wiring, raspberry pi setup, location tracking, geofences, calibration, and troubleshooting.

##  repository structure

```text
location-clock/
├── config/
│   ├── zones.example.geojson
│   └── clock_positions.example.json
├── hardware/
│   ├── README.md
│   └── diagrams/
├── software/
│   ├── main/
│   │   └── owntracks_receiver.py
│   ├── calibration/
│   │   └── calibrate_clock.py
│   └── testing/
│       ├── move_hand.py
│       └── move_hands.py
├── .gitignore
├── README.md
└── requirements.txt
```

## customization

the clock is designed to be customized ---

you can change the locations on the clock face, create your own geofences, change which hand belongs to each person, modify servo channels, create custom location states, and design your own clock face and hands

the donor clock itself is not important — the same system can be adapted to other clock cases or completely custom enclosures

##  inspiration

this project was inspired by the magical location clock concept from the harry potter series but is an independent open-source fan project and is not affiliated with or endorsed by warner bros, j k rowling, or the harry potter franchise

the software, mechanical implementation, documentation, and project branding are being developed independently

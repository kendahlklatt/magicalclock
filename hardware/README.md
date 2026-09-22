# hardware 

this folder documents the physical hardware used to build the four-hand magical location clock :)

the mechanism uses four independently controlled servos connected to four concentric rotating tubes, allowing all four clock hands to rotate around the same center point while moving independently. this way all clock hands come out from the same place on the clock, like a normal clock with only two hands. 

## how the mechanism works

each clock hand is attached to its own telescoping tube ->

the four tubes are nested concentrically so they share the same center axis while remaining mechanically independent ->

each tube is connected to a 64t driven gear ->

a separate servo drives each 64t gear using a 32t gear mounted to the servo shaft

```text
servo
  ↓
32t gear
  ↓
64t gear
  ↓
concentric tube
  ↓
clock hand
```

the 32t to 64t gear combination creates a 2:1 reduction between the servo and the clock hand

four copies of this mechanism are stacked around one concentric shaft assembly

## electronics

the current prototype uses

- raspberry pi
- pca9685 16-channel pwm servo controller
- 4 continuous rotation or sail winch servos
- separate 5v servo power supply
- jumper wires
- shared ground between the raspberry pi, pca9685, and servo power system

the raspberry pi communicates with the pca9685 over i2c

```text
raspberry pi
      │
      │ i2c
      ↓
   pca9685
   ├── channel 0 → servo 1
   ├── channel 1 → servo 2
   ├── channel 2 → servo 3
   └── channel 3 → servo 4
```

the servos should be powered from an appropriate external supply rather than directly from the raspberry pi

## current prototype parts

### control system

- raspberry pi
- pca9685 16-channel pwm servo driver
- 5v power supply for servos
- raspberry pi power supply
- jumper wires

### movement system

- 4 jx w5513 / sw5513-6ma sail winch servos
- 4 32t servo gears
- 4 64t driven gears
- 25t servo horns or compatible hubs
- concentric telescoping tubing
- washers, spacers, and mounting hardware as needed

### concentric shaft

the prototype uses telescoping tubing with the following outside diameters

- 1/16 in
- 3/32 in
- 1/8 in
- 5/32 in

additional larger telescoping sizes can be useful during prototyping

the tubes rotate independently inside one another and extend through the center of the clock face

### clock

the prototype was built inside a repurposed quartz wall clock case

the original clock movement was removed and the new servo mechanism was installed behind the clock face

a donor clock is not required and the mechanism can also be installed in a custom enclosure

## hand assembly

each clock hand is attached to a different tube in the concentric shaft

during prototyping, the tubes were staggered slightly at the front of the clock so each hand could attach to its own tube

example protrusion lengths used during testing were

```text
1/16 in tube  → 13 mm
3/32 in tube  → 11 mm
1/8 in tube   → 9 mm
5/32 in tube  → 7 mm
```

these dimensions are not strict requirements and can be adjusted for the final hand and hub design

## gear assembly

each rotating tube needs a secure connection to its 64t gear

the prototype has used temporary methods including

- heat shrink tubing to increase tube diameter
- tape shims
- servo horn hubs
- washers
- hot glue during prototyping

these methods are useful for testing but a rigid and repeatable hub is recommended for a permanent build

the gear should rotate the tube without slipping while avoiding contact with neighboring tubes

## support

the concentric shaft needs to remain centered and approximately perpendicular to the clock face

the prototype uses a stationary support tube through the mechanism to help keep the rotating tube stack aligned

the support does not rotate with the clock hands

## reducing friction

the nested tubes should rotate freely before gears and hands are installed

if one tube causes another tube to rotate, check for

- bent tubing
- burrs from cutting
- glue contacting multiple tubes
- oversized heat shrink
- gears rubbing together
- hubs touching neighboring tubes
- excessive pressure in the gear stack

tube ends should be cut cleanly and deburred before assembly

a small amount of appropriate dry lubricant can also reduce friction between nested tubes

## mechanical alignment

before software calibration, mechanically align the four hands to the same reference position

a useful workflow is

1. command the servo to a known reference position
2. power the mechanism down if physical repositioning is required
3. align the gear and hand to the desired reference
4. restore power
5. test movement
6. perform software calibration

do not force the servo or gear while it is powered

## testing for slippage

after assembly, repeatedly move a hand through several clock positions and return it to the starting position

for example

```text
home
↓
mortal peril
↓
custom location
↓
adventure
↓
home
```

if the hand returns to exactly the same position, the mechanism is behaving repeatably

if the final position gradually changes, inspect the gear and tube connections for slipping

if the final position changes depending on the direction of approach, inspect the gear train for backlash

## calibration

the exact physical position of each hand is stored in

```text
config/clock_positions.json
```

use

```bash
python software/calibration/calibrate_clock.py
```

to determine and save the correct duty-cycle value for each position

because every physical build will be slightly different, calibration values should not be copied directly from another clock

## diagrams

mechanical and wiring diagrams will be stored in

```text
hardware/diagrams/
```

planned diagrams include

- complete electronics wiring
- concentric shaft assembly
- servo and gear arrangement
- clock hand attachment
- rear mechanism layout

## prototype warning

some connections in the current prototype were intentionally made using temporary materials while the mechanism was being developed

for a permanent build, rigid hubs, secure mounting, consistent mechanical alignment, and strain relief for wiring are recommended

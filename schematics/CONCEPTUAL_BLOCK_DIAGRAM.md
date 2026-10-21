# Preliminary electronics architecture — **NOT A WIRING SCHEMATIC**

This is a functional block diagram, not build-ready pinouts, electrical ratings, or proof of safety. It is inspired by common Raspberry Pi + dedicated servo-control patterns discussed in the [Adafruit servo driver guide](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up).

```mermaid
flowchart TD
  UI["Software / expression / vision<br>Herbie repository"]
  PI["Raspberry Pi / main computer<br>model and supply to verify"]
  IF["Motor-control interface<br>candidate: driver or MCU"]
  PAN["Head pan servo<br>unselected"]
  TILT["Head tilt servo<br>unselected"]
  PSUL["Logic power domain<br>datasheet verification required"]
  PSUM["Dedicated motor supply<br>voltage & stall current unknown"]
  STOP["Physical motor-power interrupt<br>design and testing required"]
  CAD["CAD envelope / cable path<br>3D-vision repository"]
  UI --> PI
  PI -. "versioned command contract: not implemented" .-> IF
  IF -. "unverified control signal" .-> PAN
  IF -. "unverified control signal" .-> TILT
  PSUL -. "conceptual logic supply" .-> PI
  PSUM -. "conceptual motor supply" .-> STOP
  STOP -. "conceptual protected rail" .-> PAN
  STOP -. "conceptual protected rail" .-> TILT
  CAD -. "mechanical clearance to check" .-> PAN
  CAD -. "mechanical clearance to check" .-> TILT
```

**Missing decisions:** specific supplies, isolation/reference grounding approach, signal voltage compatibility, actuation driver, overcurrent protection, wire and connector ratings, servo stall currents, safe startup state, physical stop design and mechanical travel.

A browser STOP command is a software feature and **must not be presented as an independent physical safety device**. Verify designs and measurements before supplying motor power; do not connect electronics from this drawing.

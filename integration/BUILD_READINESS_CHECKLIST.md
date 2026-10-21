# Real hardware build-readiness checklist

No phase below is automatically approved. Record measured evidence in `tests/` and source links in decision records; a checked box without evidence does not establish safety.

## Gate A: component selection
- [ ] List exact controller, driver and servo model numbers and revisions
- [ ] Link manufacturer datasheets and verified connector pinouts
- [ ] Specify display, camera, microphone and power requirements
- [ ] Record acquisition status honestly in `bom/components.csv`

## Gate B: mechanical fit
- [ ] Print or acquire actual head structure and mounts
- [ ] Measure assembled head mass, center of gravity and lever arms
- [ ] Check cable bend, pinch points, physical stops and mounting hole dimensions
- [ ] Compare measured envelopes with `3D-vision/HERBIE_V1/PARTS.csv` models
- [ ] Assign CAD part IDs only after an explicit fit review

## Gate C: electrical design
- [ ] Draw real KiCad schematic with component library provenance
- [ ] Calculate worst-case current including servo stall/starting current
- [ ] Select regulated supplies, protection, wiring gauges and connector ratings
- [ ] Confirm signal voltage compatibility and ground/reference scheme
- [ ] Independently review motor-power disable / physical STOP design
- [ ] Run KiCad ERC; review every violation and note ERC is not a safety certification

## Gate D: software/fault controls
- [ ] Define command version, units, acknowledgements and timeout
- [ ] Design local controller authority over travel limits and watchdog
- [ ] Specify behavior on reboot, disconnect, out-of-range command and power dip
- [ ] Test STOP/reset state behavior using a simulator without energized actuators

## Gate E: supervised bench evidence
- [ ] Inspect polarity, continuity and shorts with power off
- [ ] Bench-test logic alone with current limiting and measured voltage
- [ ] Bench-test actuator subsystem at controlled load with physical interrupt available
- [ ] Verify safe behavior at deliberate disconnection and restart
- [ ] Record exact measurements, conditions and failures rather than only 'passed'

**Current status:** All gates pending. This is a study project, not a validated commercial robot.

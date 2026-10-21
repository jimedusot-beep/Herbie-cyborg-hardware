# STEAM learning track: build a real robot from evidence

**Audience:** beginner makers, students and volunteers. The aim is to make learning tangible while keeping simulation and live electronics clearly separated.

## What STEAM means for H.E.R.B.I.E.

| Discipline | Starter activity | Saved evidence | What it does **not** prove |
| --- | --- | --- | --- |
| **Science** | Predict and later measure how moving the head's center of mass affects servo torque | Hypothesis and measurements with units | A torque calculation is not a servo endurance test |
| **Technology** | Run an existing facial-expression demo and note software states | Screenshot and browser/test version | A digital face is not a physical display |
| **Engineering** | Draw a labeled functional block diagram; review power domains | Diagram with unknowns explicitly marked | A block diagram is not a validated circuit |
| **Art** | Design original expressions and readable emotion cues | Storyboard, mockup, accessibility notes | Visual expressiveness is not emotional understanding |
| **Mathematics** | Compute the required torque from measured mass and lever arm | Assumptions, units and calculations | A calculated minimum is not a final servo selection |

## Five evidence-based mini-lessons

### 1. Brain — simulate first
Use [Herbie](https://github.com/jimedusot-beep/Herbie) to explore facial expressions and virtual pan/tilt. Make a prediction about how a STOP command changes the simulation. Record whether the test is software-only. The two existing virtual command protocols are not interchangeable; see [protocol audit](MOTION_PROTOCOL_COMPARISON.md).

### 2. Body — dimensions and forces
Use [3D-vision](https://github.com/jimedusot-beep/3D-vision) to rotate and measure the existing provisional parts. Keep CAD units in millimeters. For a future measured head mass `m` (kg) and perpendicular lever arm `r` (m), static gravity torque in a worst-case orientation is `tau = m * 9.81 * r` N·m. Real design must account for dynamic loads, gearing, mechanical friction, mounting and suitable engineering margins. **Do not use unmeasured values as validated design inputs.**

### 3. Electronics — identify parts
Use [the BOM](../bom/components.csv) to compare candidate components. Record exact manufacturer part number, datasheet and whether the item is physically owned. Leave electrical ratings unknown until confirmed.

### 4. Integration — trace the same component
Open [system-manifest.json](../integration/system-manifest.json), find `SERVO-HEAD-PAN-001`, locate it in the electronic BOM, and observe that its CAD part is `null` pending physical fit verification. That is intentional and prevents false compatibility claims.

### 5. Quality — make a safe change
Propose a documentation or simulation-only change on a branch. Run the automated tests, explain what passed and what was not tested, and request a pull request review. Never connect live actuators as part of a beginner web demo.

## Reflection questions

1. Which results came from simulation, and which were measured on real hardware?
2. What additional data would let us select a servo responsibly?
3. If the browser freezes, what should the **local** motor controller do?
4. How could a visitor tell the difference between a proposed design and a verified robot?
5. What is the smallest next experiment that would reduce uncertainty without energizing a motor?

## Community contributions

Good first contributions: fix broken links, document datasheet links, add unit tests, improve keyboard accessibility, propose educational diagrams, or record dimensions from verified sources. Experienced reviewers can help with power design, failure analysis, KiCad checks and hardware verification plans.

Community input is evidence to examine, not automatic engineering approval. No motor actuation or physical electrical changes are authorized by this lesson.

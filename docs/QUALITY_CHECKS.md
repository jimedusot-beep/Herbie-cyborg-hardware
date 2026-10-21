# Quality checks

Run with Python 3: `python3 tests/validate_bom.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`.

These checks validate component IDs, duplicate entries, acquisition status, quantity and inventory formatting. They do **not** validate circuit safety, real component compatibility, physical fit, or KiCad designs.

Community-inspired practice: use repeatable tests and explicit maturity labels; see [ROS REP-2004](https://reps.openrobotics.org/rep-2004/), [KiCad](https://docs.kicad.org/) and the [Adafruit Learning System](https://learn.adafruit.com/).

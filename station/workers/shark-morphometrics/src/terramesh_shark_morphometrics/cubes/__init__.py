"""The calibration cubes and the scale bar, vendored unchanged from the intertidal pipeline.

`cube.py`, `markers.py` and `scale.py` are copies of photogrammetry/intertidal/intertidal/ at
commit 467692a (PR #1, as merged into claude/intertidal-photogrammetry-mission-oi06l1-r25 at
a2eadf7). The `cube-spec*.json` files (cubes 0-3) are hardware/calibration-cube/'s, and
`scale-bar-spec.json` is hardware/scale-bar/'s (#26), at the same commit. Workers are self-contained, so these are copied like kit.py rather than imported;
tests check the copies still match when the intertidal pipeline is in the same checkout.
Everything shark-specific is in ../cubescale.py.
"""
from pathlib import Path

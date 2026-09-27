"""Write the tag36h11 codes the phone reads live, for the first few cubes.

The app decodes the cube's tags on the phone to guide the sweep. It needs each tag's 8 x 8
cell pattern, the same `tag_bits` that generate.py prints; this writes them as Swift so the
two can never drift. tests/test_swift_codes.py checks the checked-in file is current.

It also writes the scale bar's four tags (hardware/scale-bar/scale-bar-spec.json), which the
phone treats as one more rigid set, `scaleBarGroup`.

Usage: python3 swift_codes.py            # cubes 0-3: tags 0-19, bottom tags 500-503, bar 100-103
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from generate import FAMILY, TAGS_PER_CUBE, bottom_tag_id, tag_bits
SCALE_BAR_GROUP = 100

def bar_plates() -> dict[int, str]:
    """The scale bar's tag ids and the plate each is on."""
    ...

def code(tag_id: int) -> int:
    """64 bits, row-major from the tag's top-left cell, most significant first; 1 = black."""
    ...

def swift(cubes: int) -> str:
    ...

def main() -> None:
    ...

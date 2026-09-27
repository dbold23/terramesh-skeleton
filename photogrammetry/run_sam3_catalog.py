"""Post-capture SAM 3 catalog pass for a TerraMesh survey folder.

Live capture on iPhone uses Neural Engine instance masks plus tracking.
This Mac pass is the exhaustive SAM 3 / 3.1 step: prompt biological vs
anthropogenic concepts on saved keyframes, then species-classify plant
crops only. Install facebookresearch/sam3 separately; this script does
not download weights.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

def main() -> int:
    ...

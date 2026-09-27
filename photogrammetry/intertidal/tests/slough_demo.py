"""The synthetic slough end to end, for looking at: the fit from 33 taps across a low tide, the
habitat now and with the sea higher. Writes waterline-demo.json and waterline-demo.png.

    PYTHONPATH=.:tests uv run python tests/slough_demo.py OUT_DIR
"""
import json
import sys
from pathlib import Path
import numpy as np
import slough
from intertidal import waterline

def main(out: Path) -> dict:
    ...

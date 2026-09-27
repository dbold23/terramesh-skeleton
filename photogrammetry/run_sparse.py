"""Bounded local RGB photogrammetry using the pinned CPU PyCOLMAP build.

Writes original COLMAP databases/models and an audit manifest. Output has unknown
metric scale and no Earth alignment. Does not fabricate or join failed submodels.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
import pycolmap
from PIL import Image

def file_hash(path):
    ...

def main():
    ...

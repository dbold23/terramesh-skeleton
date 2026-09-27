"""Render accurate orthographic previews from the exported STL print parts.

Uses a small NumPy software z-buffer, not a CAD screenshot or imagined product
render. No hardware, cord, bumper, or coating geometry is invented. The tag
STLs receive white below z=1.2 mm and black above it, matching the print swap.
Run with the package virtual environment after export_stls.py finishes.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import trimesh

def font(size, bold=False):
    ...

def matrix(rotation=None, translation=None):
    ...

def face_matrices():
    ...

def load_parts():
    ...

def assemble(parts, exploded=False):
    ...

def render_mesh(parts, eye, exploded=False, size=(1500, 1280)):
    ...

def single(parts, filename, eye, title, subtitle, exploded=False):
    ...

def main():
    ...

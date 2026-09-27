"""Write the tiled cube's Bambu Studio 3MF: the white core and the five two-colour tag tiles on one plate.

    python3 make_tiled_3mf.py        # white on filament 3, black on 4

Needs OpenSCAD on PATH. The plate holds two objects: the core (socket face down, white) and
the tiles (face down, a white body part and a black ink part), so both print in one go. No
printer or filament profile is included, but each object carries the few settings this print
needs as per-object overrides (PRINT_SETTINGS), so they apply whatever profile is loaded.
"""
from __future__ import annotations
import argparse
import tempfile
import uuid
import zipfile
from pathlib import Path
from make_3mf import CONTENT_TYPES, CORE, IDENTITY, PRINT_SETTINGS, PROD, Mesh, export_stl, mesh_xml, read_ascii_stl, rels

def shifted(mesh: Mesh, dx: float, dy: float, dz: float) -> Mesh:
    ...

def write_bambu(objects: dict[str, list[tuple[str, Mesh, int]]], places: dict[str, tuple[float, float]], out: Path) -> None:
    ...

def main() -> None:
    ...

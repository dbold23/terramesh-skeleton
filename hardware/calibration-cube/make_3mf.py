"""Write a two-colour 3MF of the cube: one object, a white body part and a black ink part.

    python3 make_3mf.py                                   # Bambu Studio / Orca, six tags, filaments 3 and 4
    python3 make_3mf.py --bottom socket                   # five tags and the pole socket
    python3 make_3mf.py --cube-index 2                    # cube 2 (tags 10-14 and 502): calibration-cube-2.3mf
    python3 make_3mf.py --body-filament 1 --ink-filament 2
    python3 make_3mf.py --format prusa -o cube-prusa.3mf  # PrusaSlicer

Needs OpenSCAD on PATH. Each format uses that slicer's own project layout, so the
file opens as one object with the body and ink already on their filaments:

- bambu: part meshes in 3D/Objects/object_1.model, assembled by components, with
  per-part filaments in Metadata/model_settings.config. No printer or filament
  profile is included, so the slicer keeps the ones already loaded; the object
  carries PRINT_SETTINGS as per-object overrides.
- prusa: one mesh with per-part triangle ranges and extruders in
  Metadata/Slic3r_PE_model.config, plus white and black core 3MF materials.
"""
from __future__ import annotations
import argparse
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path

def export_stl(scad: Path, part: str, out: Path, defines: dict[str, str] | None=None) -> None:
    ...

def read_ascii_stl(path: Path) -> Mesh:
    """Vertices (deduplicated) and triangles from an ASCII STL."""
    ...

def rels(target: str) -> str:
    ...

def mesh_xml(mesh: Mesh, dz: float=0.0, material: int | None=None, offset: int=0) -> tuple[str, str]:
    ...

def write_bambu(meshes: dict[str, Mesh], filaments: dict[str, int], out: Path, bed_xy: float, name: str='calibration-cube', settings: dict[str, str] | None=None) -> None:
    ...

def write_prusa(meshes: dict[str, Mesh], filaments: dict[str, int], out: Path) -> None:
    ...

def main() -> None:
    ...

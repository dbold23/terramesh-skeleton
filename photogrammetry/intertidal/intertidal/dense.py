"""Dense point cloud with OpenMVS, on the Mac's CPU.

COLMAP's own dense stereo needs CUDA, so a Mac mini can't run it. OpenMVS can: it reads the
undistorted COLMAP model, computes a depth map per frame and fuses them into a point cloud
that is far denser than the sparse model, which matters most on crevice walls, where the
sparse model has few points. The dense cloud is in the same frame as the sparse model, so
the cube's similarity takes it to millimetres unchanged.

OpenMVS is a separate install (it isn't on PyPI). Point `--openmvs-bin` or `OPENMVS_BIN` at
the folder holding `InterfaceCOLMAP` and `DensifyPointCloud`, or put them on PATH.
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

class OpenMVSMissing(RuntimeError):
    ...

def find(bin_dir: Path | str | None=None) -> Path:
    """The folder holding the OpenMVS tools this module runs."""
    ...

def version(bin_dir: Path) -> str:
    """OpenMVS prints its version in the banner of any tool ("OpenMVS x64 v2.3.0")."""
    ...

def densify(sparse_dir: Path, frames_dir: Path, work: Path, bin_dir: Path, resolution_level: int=1, max_resolution: int=2560, log=None) -> Path:
    """Returns the dense PLY, in the sparse model's frame."""
    ...

def _run(command: list, cwd: Path, log) -> None:
    ...

"""Intertidal photogrammetry: phone video + calibration cube -> crevice dimensions in mm.

  python -m intertidal run capture.mov out/            # all steps below
  python -m intertidal from-export survey.zip out/     # same, from the app's intertidal sweep clips
  python -m intertidal frames capture.mov out/frames   # sharp, unclipped frames
  python -m intertidal sfm out/                        # COLMAP + cube scale (+ OpenMVS) -> scale.json, *-mm.ply
  python -m intertidal apply-scale dense.ply out/scale.json dense-mm.ply
  python -m intertidal measure out/sparse-mm.ply [--rim rim.json | --seed x,y,z] [--cameras out/cameras-mm.json]
  python -m intertidal pick out/                       # pick.html: click the crevice when the search misses
  python -m intertidal mesh out/                       # textured mesh (mesh/mesh-mm.ply) and mesh/crevice.usdz
  python -m intertidal tide out/                       # heights above MLLW, datum lines, hours under water
  python -m intertidal reef strip1/ strip2/ ... --out reef/   # many strips joined through shared cubes, tide zones
  python -m intertidal reef-from-export survey.zip reef/      # every sweep of a survey as a strip, then the reef
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from . import frames, measure, ply
from .cube import CUBE_FOLDER, SCALE_BAR_SPEC, Cube, spec_paths
from .scale import Similarity

def _cube(args) -> Cube:
    """Every cube the run may see: spec files, or folders of them (all their cube-spec*.json)."""
    ...

def cmd_frames(args) -> None:
    ...

def cmd_sfm(args) -> dict:
    ...

def _dense(args, transform: Similarity, frames_dir: Path, progress) -> dict:
    """OpenMVS densification, when asked for or when it is installed."""
    ...

def _cloud_for_measuring(out: Path) -> Path:
    ...

def cmd_apply_scale(args) -> None:
    ...

def cmd_measure(args) -> dict:
    ...

def _seeds(args, cloud: Path) -> list[tuple[str, np.ndarray]]:
    """Where the automatic search may start, best first: a given --seed (or the phone's
    lock-on), then the point the cameras were aimed at, then the cube."""
    ...

def _radii(args) -> list[float]:
    """Search radii to try round a seed: --radius, then 100 mm wider at a time up to --max-radius."""
    ...

def _search(args, xyz: np.ndarray, cameras: np.ndarray) -> dict:
    """The nearest crevice to the first seed that gives an opening inside the search circle.

    Round each seed the circle grows until the opening is closed inside it: a crevice wider
    than --radius is measured whole rather than clipped. The cube is often beside the crevice
    but on other rock, or on the floor below an overhang, so a sweep's own aim is tried before
    it. If every seed gives a clipped opening, the first result stands, with its warning."""
    ...

def _measure_or_explain(args) -> None:
    """The scale is the part that must succeed; an automatic mouth search can fail on a
    scene with no clear cavity, and that should leave the scaled cloud usable."""
    ...

def cmd_run(args) -> None:
    ...

def _record_and_compare(args) -> dict:
    """With --crevice-id: write the visit's record to out/record, and compare it with the
    latest earlier visit of the same crevice in --library, if there is one."""
    ...

def _print_comparison(result: dict) -> None:
    ...

def cmd_record(args) -> None:
    ...

def cmd_compare(args) -> None:
    ...

def cmd_library_add(args) -> None:
    ...

def cmd_library_identify(args) -> None:
    ...

def cmd_library_list(args) -> None:
    ...

def _up_from_arkit(views: list[dict], priors: dict) -> np.ndarray | None:
    """Gravity's up (ARKit's +Y) in the cube frame, from the frames with both an ARKit and a
    photo pose."""
    ...

def _save_priors(out: Path, priors: dict) -> None:
    """Keep the kept frames' ARKit poses beside the run, so later steps (the mesh's gravity)
    do not need the export again. Written even when there are none, to say so."""
    ...

def _saved_priors(out: Path, export_path: Path | None=None) -> dict:
    """The ARKit poses of a finished run's frames: from arkit-poses.json, or read again from the
    survey export (`export_path`, or the copy unpacked into the run)."""
    ...

def _mesh(args) -> dict | None:
    """A textured mesh of the run, in cube mm, and a USDZ of it. Never fails the run: the
    measurements do not depend on it."""
    ...

def _build_mesh(args) -> dict:
    ...

def _export_folder(out: Path, export_path: Path | None=None) -> Path | None:
    """The survey export a run came from: `export_path`, or the copy unpacked into the run."""
    ...

def cmd_tide(args) -> dict:
    """Heights above the tide station's MLLW for the whole scan, the datum lines on it and hours
    a day under water. See tide.py for how the model is tied to the datum."""
    ...

def _tide(args) -> None:
    """The tide step inside from-export. Never fails the run."""
    ...

def _load_strip(run: Path, voxel_mm: float):
    """A finished run as a reef strip: its cloud, where its cubes sit, gravity, its ARKit fit,
    its tracking sessions and its tie to the tide."""
    ...

def cmd_reef(args) -> dict:
    """Join many strips into one levelled reef model and map its tide zones. See reef.py."""
    ...

def _reef_waterline(args, tie, local, use_local, series, datums, year, zones, zonation, notes):
    """The reef's (or slough's) own tide with flood and ebb and a low-tide floor where the taps show
    them, and its habitats now and with the sea higher: the reef.json `waterline` section, and
    waterline.png."""
    ...

def cmd_heat(args) -> dict:
    """Days in the forecast when a low tide leaves a band out in hot sun, from a finished reef."""
    ...

def _reef_zonation(strips, placed, level, visits, wet, zones, tie, local, use_local, series, datums, year, notes):
    """The reef's bands of life and wet lines, set against the waterline and the station's datums:
    (the reef.json section, band lines and tap dots for the map, cell colours by biological zone)."""
    ...

def _still_water_z(strip, visit, tie, local, use_local, series) -> tuple[float | None, str | None]:
    """The reef z of the still water while a strip was filmed, from the best thing that knew it."""
    ...

def cmd_reef_from_export(args) -> dict:
    """Every sweep of a survey processed as its own strip, then joined into the reef."""
    ...

def _pick_page(args) -> None:
    """pick.html beside the results, to check what was measured and to pick the crevice by hand."""
    ...

def cmd_mesh(args) -> None:
    ...

def cmd_diagnose(args) -> None:
    ...

def cmd_pick(args) -> None:
    ...

def cmd_from_export(args) -> None:
    ...

def _phone_guide(args, clips) -> dict | None:
    """The crevice the operator locked on to in the app, placed in the cube frame.

    The lock-on point is in ARKit's world; the frames that have both an ARKit pose and a photo
    pose give the similarity into cube millimetres (the same fit the LiDAR check uses). Unless
    --seed was given, the automatic crevice search starts there instead of at the cube."""
    ...

def _report_phone_guide(args, guide: dict) -> None:
    """Put the phone's live estimate beside the Mac's own numbers in crevice.json."""
    ...

def _lidar(args, clips) -> dict | None:
    """Place the sweep's LiDAR depth in the cube frame; check the photo model and fill its gaps."""
    ...

def main(argv: list[str] | None=None) -> None:
    ...

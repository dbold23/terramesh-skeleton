"""What happened on a sweep, from the export alone: for a field or desk test that went wrong.

    intertidal diagnose survey.zip [--out folder]

Nothing here reconstructs anything. It reads what the phone wrote beside each sweep and
answers the questions a test raises:

- **Lag.** The pose track has one row per recorded frame with ARKit's timestamp. The app
  records clip frames on the thread that also runs the live guide, so a stall there shows as a
  gap between rows: frames per second, gaps over 100 ms, the longest.
- **How the phone moved.** Path length and speed, the range to the lock-on point, and the cone
  of directions it was looked at from (the angle between the lock's normal and each camera).
  The back of a deep opening is seen only from inside that cone.
- **Blur.** How fast the lock-on point crossed the image, and the smear that makes at 1/60 s
  and 1/30 s exposures (4 px or less is sharp to the guide). The phone's own share of sharp
  frames is in the guide summary.
- **The guide.** The phone's summary as saved: coverage, opening size, deepest, sides seen,
  cube faces.
- **LiDAR at the opening.** Around the lock-on point in each depth frame: how many returns were
  missing or low confidence, and how far behind the face the rest sat. Returns far behind the
  face are the back of a deep hole, or the background seen through something clear: LiDAR and
  photos both pass through glass and clear plastic.

The report is JSON (`diagnose.json`) with a plain summary beside it (`diagnose.txt`).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from . import export, lidar
GAP_S = 0.1
SHARP_PX = 4.0
STRAIGHT_IN_DEG = 12.0
WINDOW_MM = 60.0
BEHIND_LIMIT_MM = 400.0

def _round(value, places=3):
    ...

def timing(clip: export.SweepClip, frame_rate: float | None) -> dict:
    ...

def motion(clip: export.SweepClip) -> dict:
    ...

def _pixel(pose: export.FramePose, world: np.ndarray) -> np.ndarray | None:
    ...

def depth_at_lock(clip: export.SweepClip) -> dict:
    ...

def diagnose(export_path: Path, out: Path) -> dict:
    ...

def summary_lines(report: dict) -> list[str]:
    ...

"""Build a synthetic TerraMesh survey export of the ray-cast crevice scene.

    PYTHONPATH=.:tests python3 tests/make_export.py out/survey.zip [--frames 60] [--no-poses] [--lidar]

The ZIP holds what the app writes for an intertidal sweep: `manifest.json`, one
`clips.jsonl` line, `clips/<id>.mov` and, unless --no-poses, `clips/<id>.poses.jsonl`.
The poses are given ARKit's conventions and deliberately imperfect: a rotated, offset world
in metres, a 1.5% scale error and 2 mm of jitter, so the run shows the cube, not ARKit,
setting the scale. With --lidar it also writes `clips/<id>.depth`: 256 x 192 scene depth for
every sixth frame, in true metres with 2 mm of noise, as a LiDAR phone would.
"""
from __future__ import annotations
import argparse
import json
import tempfile
import uuid
import zipfile
from pathlib import Path
import cv2
import numpy as np
from intertidal import lidar
from scene import render, render_depth, sweep
W, H, F = (960, 720, 760.0)
DEPTH_W, DEPTH_H = (256, 192)
ARKIT_SCALE_ERROR = 1.015

def arkit_world(seed: int=7):
    ...

def depth_frames(path, stride: int=6, seed: int=11) -> list:
    ...

def arkit_pose_lines(path, R_a, t_a, rng) -> list[str]:
    ...

def build(out: Path, frames: int=60, poses: bool=True, depth: bool=False) -> dict:
    ...

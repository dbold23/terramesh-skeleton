"""Synthetic cube renders and crevice clouds with exactly known geometry."""
from __future__ import annotations
import json
import cv2
import numpy as np
from intertidal.cube import DEFAULT_SPEC
W, H = (1920, 1080)

def look_at(eye: np.ndarray, target=np.zeros(3), up=np.array([0, 0, 1.0])) -> tuple[np.ndarray, np.ndarray]:
    """camera_from_world rotation and translation for an OpenCV camera."""
    ...

def face_texture(tag: dict, px_per_cell: int=40) -> np.ndarray:
    """10 x 10 cells: one white quiet-zone cell around the 8 x 8 tag."""
    ...

def render_cube(R: np.ndarray, t: np.ndarray, seed: int=0, blur: float=0.0) -> np.ndarray:
    ...

def render_cubes(R: np.ndarray, t: np.ndarray, cubes: list, seed: int=0, blur: float=0.0) -> np.ndarray:
    """Several cubes in one frame. Each is (spec, R_k, t_k, size): world = R_k @ (size * cube) + t_k,
    where `size` other than 1 stands for a cube printed too large or small."""
    ...

def project(points: np.ndarray, R: np.ndarray, t: np.ndarray) -> np.ndarray:
    ...

def crevice_cloud(width=120.0, height=40.0, depth=90.0, centre=(110.0, 0.0), spacing=1.5, extent=220.0, seed=0, relief=0.0, infill=None) -> np.ndarray:
    """Rock face z = 0 facing +z, with a rectangular slot cut into it.

    The slot's mouth is `width` along x and `height` along y, centred at
    `centre`; its walls run `depth` mm into the rock (towards -z).
    `relief` adds smooth bumps of that height to the face away from the slot.
    `infill=(x_split, fill_depth)` fills the slot below x < x_split up to
    `fill_depth` mm behind the mouth, like sediment in one end."""
    ...

def overhang_scene(spacing=2.0, seed=0):
    """Cube frame: the cube sits on a sand floor z = -20. The crevice is a slot in a rock face
    y = 80 rising from the floor, filmed from the side (cameras level, looking +y). The floor has
    a shallow pocket beside the cube."""
    ...

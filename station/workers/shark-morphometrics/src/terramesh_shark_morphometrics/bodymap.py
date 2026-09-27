"""The shark's skin, unrolled into body coordinates from the walk-round stills.

The walk round the animal is the one capture. Its posed stills give the landmarks and the
measurements (triangulate.py), and the same stills and the same landmarks give this: a picture
of each side of the animal in the shark's own coordinates, where a column is a fraction of
precaudal length from the snout and a row is an angle round the body from the midline of the
back. A spot lands on the same pixel of the map whoever took the pictures, from whatever
distance and angle, so the matcher compares like with like and the perspective of any one
photograph is gone.

The body is modelled as a smooth fusiform solid of elliptical cross-section laid along the
snout-to-caudal axis, sized by precaudal length. It is a generic shape, not the animal's own
surface: fins are not in it, and where the real flank bulges past the model the map is shifted
by a few millimetres. When an Object Capture mesh of the encounter exists, it can replace the
model; until then every map says it was made on the generic body.

Which way is which needs two landmarks. With the snout tip and the upper caudal origin picked
(pick.html, the same picks the measurements use), the axis, the head end and so left from right
are known, and a dorsal landmark or gravity gives up. Without picks the axis is estimated from
the walk itself, perpendicular to the direction the photographer mostly faced, and the head end
is unknown: the maps are then made both ways round and each is labelled as an assumption, so a
matcher can try both and nothing is filed under the wrong flank.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from .cameras import Still
GREY = 128

def profile(s: np.ndarray) -> np.ndarray:
    """Body depth along the axis, 0 at the snout, 1 at the deepest point (about 0.38 PCL),
    tapering to a quarter at the caudal origin. A smooth fusiform curve, not a measured outline."""
    ...

@dataclass
class BodyFrame:
    """The shark's own axes in the survey's ARKit world."""
    snout: np.ndarray
    forward: np.ndarray
    up: np.ndarray
    pcl: float
    mission: str
    source: str
    head_known: bool

    @property
    def right(self) -> np.ndarray:
        ...

    def flipped(self) -> 'BodyFrame':
        """The same axis the other way round: the head at the other end."""
        ...

    def surface(self, s: np.ndarray, phi_degrees: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Points on the model body and their outward normals, for body coordinates s (fraction of
        PCL) and phi (degrees round the body from the back). Returns (N x 3, N x 3)."""
        ...

    def to_json(self) -> dict:
        ...

def _unit(v: np.ndarray) -> np.ndarray | None:
    ...

def frame_from_landmarks(points: dict[str, np.ndarray], mission: str) -> BodyFrame | None:
    """The body frame from picked landmarks, or None without a snout and a caudal landmark."""
    ...

def frame_from_walk(stills: list[Still], mission: str, total_length: float | None=None) -> BodyFrame | None:
    """A rough body frame from the walk alone: the animal lies where the cameras' lines of sight
    meet, flat, and across the direction the photographer mostly faced. Which end is the head is
    not known."""
    ...

def person_mask(path: Path | None, still: Still, size: tuple[int, int]) -> np.ndarray | None:
    """The handlers' mask (white = person, upright like the displayed still) in the still's stored
    pixels at `size`, widened by about 1 % so a glove's edge does not survive. None if absent."""
    ...

@dataclass
class BodyMap:
    view: str
    image: Image.Image
    coverage: float
    stills_used: int
    assumed_side: bool
    main_still: Path | None = None

def bilinear(array: np.ndarray, uv: np.ndarray) -> np.ndarray:
    """RGB at sub-pixel positions (N x 2, x then y) of an H x W x 3 picture."""
    ...

def render(stills: list[Still], frame: BodyFrame, view: str, *, width: int=1024, height: int=320, min_facing: float=0.35, work_edge: int=2400, masks: dict[str, Path] | None=None) -> BodyMap:
    """One view's body map. Each map pixel is taken from the still that saw that bit of skin most
    squarely (the largest cosine between the surface normal and the line to the camera, at least
    `min_facing`), never from under a handler's mask. Pixels no still saw are flat grey, which
    the matchers find nothing in."""
    ...

def render_views(stills: list[Still], frame: BodyFrame, views: list[str], *, min_coverage: float=0.3, masks: dict[str, Path] | None=None, **kwargs) -> list[BodyMap]:
    """Maps of each requested view (leftFlank, rightFlank, dorsal, head) that the walk saw enough
    of. With the head end unknown, every view is also made with the axis turned round, and both
    are marked as assumptions: the walk saw one flank, and which one depends on where the head is."""
    ...

def masks_in(snapshot: Path) -> dict[str, Path]:
    """The export's handler masks by frame id (upper case)."""
    ...

def body_maps(snapshot: Path, stills: list[Still], mission: str, landmarks: dict[str, np.ndarray] | None=None, total_length: float | None=None, views: list[str] | None=None, min_coverage: float=0.3) -> tuple[BodyFrame | None, list[BodyMap]]:
    """The body frame (from landmarks when they fix it, else from the walk) and the maps the walk
    saw enough of. The one entry point both the measuring and the matching workers use, so the
    two always unroll the same skin the same way."""
    ...

def write_maps(folder: Path, frame: BodyFrame, maps: list[BodyMap]) -> list[dict]:
    """Saves each map as a JPEG under `folder` and returns their descriptions."""
    ...

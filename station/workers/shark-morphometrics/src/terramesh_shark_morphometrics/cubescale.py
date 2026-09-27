"""Scale from calibration cubes or the scale bar set beside the animal.

ARKit's world is metric only as far as its visual-inertial tracking gets the scale right, which
is a couple of percent on land and can be worse on a rolling deck, where the IMU feels the swell
that the camera does not see. A 40 mm calibration cube is an object of known size in that same
world. Its tag corners are triangulated from the frames' ARKit poses, and the intertidal
pipeline's shared-scale solve (vendored in cubes/) fits one scale with a separate pose per cube:
that scale says how many real metres one ARKit metre is.

The scale bar (two tag plates 882 mm apart on a 1 m steel rule, clipped to the stretcher pole) is
one more rigid tag set in the same solve. Its baseline is more than twenty times a cube's, so when
both its plates are seen it sets the scale, and the solver leaves out any cube that reads more
than 1 % from it. Its length comes from the rule's graduations, good to `bar_length_uncertainty`.

A cube whose corners fit badly (it was knocked during the pass, or two cubes carry the same
number) is left out before the shared solve. With three or more cubes the solver itself drops
one that disagrees with the rest. Cubes that disagree by more than `cube_max_disagreement` and by
well over their own scatter widen the uncertainty to cover the gap, because head and tail cubes
that disagree mean ARKit's scale drifted along the animal. With no usable cube or bar the
measurement falls back to ARKit's own scale and its stated uncertainty.

The scale's uncertainty is a jackknife over the frames that saw the cubes (so errors shared by
every corner of one frame, such as that frame's pose, count once per frame, not once per
corner), plus the cubes' print tolerance, or the bar's length tolerance, in quadrature.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
import numpy as np
from PIL import Image
from .cameras import Still
from .cubes import BAR_SPEC, FOLDER
from .cubes.cube import Cube, spec_paths
from .cubes.markers import Detection, detect
from .cubes.scale import ScaleReport, View, solve
MAX_SCALE_CHANGE = 0.15

def all_cubes() -> Cube:
    """Cubes 0-3 and the scale bar as one Cube: tags 5n..5n+4 and 500+n are cube n, tags
    100-103 the bar (set SCALE_BAR_GROUP)."""
    ...

def bar_used(cube: Cube, report: ScaleReport) -> bool:
    """The bar sets the scale only with both plates located, as the solver decides."""
    ...

@dataclass
class CubeResult:
    index: int
    frames: int
    tags: list[int]
    corner_rms_mm: float
    own_scale_pct: float
    centre: np.ndarray
    used: bool = False

    def to_json(self) -> dict:
        ...

@dataclass
class Scale:
    factor: float
    sigma: float
    source: str
    cubes: list[CubeResult]
    solver: dict | None = None

    def to_json(self) -> dict:
        ...

def gray(still: Still) -> np.ndarray:
    """The stored pixels, never turned by EXIF: the intrinsics describe these."""
    ...

def find(stills: list[Still], cube: Cube) -> list[tuple[Still, Detection]]:
    """Every frame that shows at least one cube tag, with the tags it shows."""
    ...

def without(sightings: list[tuple[Still, Detection]], cube: Cube, dropped: set[int]) -> list[View]:
    ...

def jackknife(views: list[View], cube: Cube, scale: float) -> float | None:
    """Relative standard error of the scale from leaving out one frame at a time."""
    ...

def arkit_centre(report: ScaleReport, index: int) -> np.ndarray:
    ...

def cube_scale(stills: list[Still], params: dict, warn) -> Scale:
    ...

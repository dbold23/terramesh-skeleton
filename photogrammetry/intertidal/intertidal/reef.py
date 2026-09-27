"""A whole reef from many strips: join the runs through the cubes they share, level the result,
tie it to the tide once, and map the reef's tide zones.

A crevice is one 45 s sweep. A reef flat is tens of metres, too big for one sweep and one
model, so it is filmed as overlapping strips at low tide with cubes left in place between
them. Each strip is processed on its own (`intertidal from-export --clip`), which gives it its
own cube-millimetre frame. This module puts every strip into one frame:

- **Shared cubes.** A cube seen in two strips has a known pose in each (scale.json's
  `frame_from_cube`), so one shared cube fixes the rigid join between the strips; two or more
  also check it (a cube knocked between strips shows as a residual and is dropped). The cubes
  set each strip's scale, so joins are rigid: nothing is rescaled.
- **ARKit.** Strips filmed in one tracking session share ARKit's world, which joins them when
  they share no cube; the join is then refined on the overlapping rock (ICP), since ARKit
  drifts by about 1% of the distance walked.

The joined model is levelled (+Z is gravity's up, averaged over the strips) with the
reference strip's frame cube at the origin. Every Water's edge tap in every strip then ties the
one model to the station's MLLW, so heights, datum lines and hours under water are consistent
across the reef, and strips whose ties disagree are named.

The reef's life gives a second, local datum. Band edge taps on the phone mark the upper limits
of the bands (barnacles, rockweed, mussels, surfgrass), which set where the animals and plants
find the zones, however the tide station says the water moves; the wet line, from dark wet rock
in each strip's colours, measures how far above the still water the waves reached while it was
filmed. Both are set against the Water's edge taps and the station's datums.

Nothing here carries a location: the model is in millimetres about a cube, and the survey's
public tile stays the neighbourhood cell (res 7) its strips already carry. Crevices are not
marked on the reef outputs.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
from .scale import Similarity
CUBE_EDGE_MM = 40.0
MOVED_CUBE_MM = 10.0
ARKIT_ICP_MAX_MM = 150.0
ARKIT_ICP_MAX_DEG = 3.0
TIDE_DISAGREE_SIGMA = 2.0

@dataclass
class Strip:
    """One processed run, as the reef needs it."""
    name: str
    points: np.ndarray
    colours: np.ndarray | None
    cubes: dict[int, np.ndarray]
    up: np.ndarray | None
    arkit: Similarity | None = None
    tide: dict | None = None
    mesh_tile: dict | None = None

@dataclass
class Join:
    strip: str
    to: str | None
    method: str
    residual_mm: float | None = None
    icp_mm: float | None = None
    overlap_mm: float | None = None

    def to_json(self) -> dict:
        ...

def _corners() -> np.ndarray:
    ...

def _apply(m: np.ndarray, points: np.ndarray) -> np.ndarray:
    ...

def rigid(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """4x4 rotation and translation taking src onto dst (Kabsch), no scale."""
    ...

def join_by_cubes(a: Strip, b: Strip) -> tuple[np.ndarray, list[int], float, list[int]] | None:
    """The rigid transform taking strip b's frame into strip a's, from the cubes both saw: the
    transform, the cubes used, the RMS of their corners and any cube dropped as moved."""
    ...

def join_by_arkit(a: Strip, b: Strip) -> np.ndarray | None:
    """Rigid join through ARKit's world, when both strips were filmed in one tracking session.
    Each strip's cube fixed its own scale, so only the rotation and the place are taken."""
    ...

def _sample(points: np.ndarray, n: int, seed: int=0) -> np.ndarray:
    ...

def _overlap_gap(moved: np.ndarray, placed: np.ndarray, reach_mm: float=50.0) -> float | None:
    """Median distance from a strip's points to the surface of the strips already placed (point
    to plane, so point spacing doesn't count), over the part that overlaps them."""
    ...

def _rotation_deg(m: np.ndarray) -> float:
    ...

def place(strips: list[Strip], reference: str | None=None) -> tuple[dict[str, np.ndarray], list[Join]]:
    """Every strip's frame into the reference strip's frame, breadth first, preferring cube joins
    (and among them, joins through more cubes) over ARKit joins."""
    ...

def levelled(up: np.ndarray, forward: np.ndarray=np.array([1.0, 0, 0])) -> np.ndarray:
    """A rotation taking `up` to +Z, keeping `forward` (projected level) along +X."""
    ...

@dataclass
class TideTie:
    """Height above MLLW (m) = offset_m + z_mm / 1000 in the levelled reef frame."""
    offset_m: float
    uncertainty_m: float | None
    lower_limit: bool
    station: str | None
    strips: list[dict]
    notes: list[str]

def tie_to_tide(strips: list[Strip], placed: dict[str, np.ndarray], level: np.ndarray, station_to_site_m: float) -> TideTie | None:
    """One MLLW tie for the reef from every strip's own (tide.json). A strip's tie says
    height = offset + (p . up) / 1000 at its own points; carried into the reef frame at the
    strip's middle, each gives the reef's offset. Waterline ties are averaged by their
    uncertainty, keeping the station-to-site term, which no number of taps averages away;
    with only dry scans (lower limits) the highest bound holds."""
    ...

@dataclass
class Zones:
    cell_mm: float
    heights: np.ndarray
    origin: np.ndarray
    area_m2: float

def plan_grid(points: np.ndarray, cell_mm: float=50.0) -> Zones:
    """The reef seen from above: the highest point in each cell, which is the surface a
    walker stands on and the water covers last."""
    ...
LOCAL_MIN_MARKS = 6
LOCAL_MIN_MINUTES = 45.0
LOCAL_MIN_RANGE_M = 0.25
LOCAL_MAX_LAG_MIN = 120

@dataclass
class LocalTide:
    """The reef's water as its own waterline showed it, against the station (NOAA's subordinate
    station method): site water z (reef mm) = intercept_mm + 1000 * ratio * station(t - lag).
    The lag and the range ratio are measured by the taps alone; the intercept is also what ties
    the model to the station, so an absolute offset (wave setup, water piled up by wind) needs a
    height from outside, such as an RTK point or a tidal benchmark."""
    usable: bool
    reason: str | None
    marks: int
    minutes: float
    station_range_m: float
    ratio: float | None = None
    lag_min: float | None = None
    intercept_mm: float | None = None
    rms_m: float | None = None
    ratio_sd: float | None = None
    lag_sd_min: float | None = None
    source: str | None = None

    def station_level(self, z_mm: np.ndarray) -> np.ndarray:
        """The station's level (m above its MLLW) at which the reef's water reaches z."""
        ...

    def z_for(self, station_m: float) -> float:
        ...

    def to_json(self) -> dict:
        ...

def _fit_at(marks: np.ndarray, times: np.ndarray, levels: np.ndarray, lag_s: float):
    ...

def _best_lag(marks: np.ndarray, times: np.ndarray, levels: np.ndarray):
    ...

def fit_local_tide(marks: list[tuple[float, float, str]], times: np.ndarray, levels: np.ndarray, source: str) -> LocalTide:
    """Fit the reef's lag and range ratio to the station from the waterline taps."""
    ...

def zone_areas(station_level_m: np.ndarray, cell_m2: float, datums: dict[str, float], year: np.ndarray | None) -> dict:
    """Plan area between the datum lines and in bands of hours a day under water, from each
    cell's height expressed as the station level at which water reaches it."""
    ...

def render_plan(path, zones: Zones, rgb_cells: np.ndarray | None, contours: dict[str, float], cubes: dict[int, np.ndarray], title: str, note: str, px_per_cell: int=4, hours_legend: bool=False, bands: list[tuple[str, float, tuple]]=(), taps: list[tuple[np.ndarray, tuple]]=()) -> None:
    """A top-down map of the reef: cells coloured, datum lines drawn, band edges drawn in their
    colours with their taps as dots, cubes numbered, 1 m bar."""
    ...
WET_BIN_MM = 25.0
WET_MIN_POINTS_PER_BIN = 30
WET_MAX_CONTRAST = 0.85
WET_MIN_R2 = 0.6
WET_MAX_WIDTH_MM = 120.0

@dataclass
class BandEdge:
    band: str
    z_mm: float
    xy_mm: np.ndarray | None
    strip: str
    time: str | None

def _height_shift(strip: Strip, placed: dict[str, np.ndarray], level: np.ndarray) -> tuple[float, float]:
    """(the strip's middle along its own up, the same point's reef z): a height in the strip's
    own frame less the first plus the second is its reef z."""
    ...

def band_edges(strips: list[Strip], placed: dict[str, np.ndarray], level: np.ndarray) -> list[BandEdge]:
    """Every strip's band edge taps (its tide.json `bands`), in the reef frame."""
    ...

def band_levels(edges: list[BandEdge]) -> dict[str, dict]:
    """Each band's upper limit over the reef: the median of its taps, and how far they spread.
    Taps of one band at different heights are the point: the band climbs where waves reach higher."""
    ...

def zone_boundaries(levels: dict[str, dict]) -> tuple[list[tuple[str | None, str | None, float, float]], list[str]]:
    """The biological zones from the tapped band edges: (upper band, lower band, top z, bottom z),
    top first. Edges out of their usual order are named rather than reordered."""
    ...

def zone_name(upper: str | None, lower: str | None) -> str:
    ...

def biological_zone_areas(cell_z: np.ndarray, cell_m2: float, zones) -> dict[str, float]:
    ...

@dataclass
class WetLine:
    """Where a strip's rock turns from dark (wet) to pale (dry) with height, in reef z."""
    strip: str
    found: bool
    reason: str | None = None
    z_mm: float | None = None
    sd_mm: float | None = None
    width_mm: float | None = None
    contrast: float | None = None
    r2: float | None = None

    def to_json(self) -> dict:
        ...

def _brightness_by_height(z: np.ndarray, luminance: np.ndarray, lo: float, hi: float):
    ...

def _best_step(centres: np.ndarray, medians: np.ndarray, counts: np.ndarray):
    """The split of height bins into a darker lower part and a paler upper part that fits best."""
    ...

def wet_line(name: str, z: np.ndarray, rgb: np.ndarray | None, seed: int=0) -> WetLine:
    """Wet rock is darker than dry: find the height where a strip's brightness steps up.

    Brightness is binned by reef height and fitted with a step (then a logistic, for its
    width). It is a wet line only when the step is sharp and strong; a slow darkening with
    height is shade or a change of rock. Dark life (a mussel bed, black lichen) also makes a
    step, which is why the band edges are set beside it."""
    ...

"""Crevice dimensions from a scaled point cloud.

Everything here works in cube millimetres. A crevice is described relative to
its mouth plane: the plane of the surrounding rock face at the opening.

  opening width    long side of the smallest rectangle around the mouth
  opening height   short side of that rectangle; for a horizontal slot under
                   a ledge this is the roof-to-floor gap an abalone sits in
  depth            how far the observed interior reaches behind the mouth
                   (deepest point, 95th percentile, and the mean and median
                   over the mouth: how deep the crevice is on average)
  mouth area       area of the mouth outline, and its perimeter
  volume           open space between the mouth plane and the deepest
                   observed surface, over the cells that were actually seen
  surface area     area of the interior surface seen through the mouth,
                   walls included; rugosity is that over the mouth area

Rugosity here counts the walls, so a deep, narrow crevice has a high rugosity even when
its rock is smooth: a 120 x 40 mm slot 90 mm deep with flat walls has 7.0. To tell the
crevice's form from the roughness of its rock, `rugosity_shape` repeats the area over a
depth surface smoothed across about a centimetre, and `rugosity_texture` is rugosity over
that: the share added by bumps finer than a centimetre. `depth_noise_mm` is the scatter of
points about their cell's typical depth, which is how noisy the cloud itself is.

A dense cloud from field video is noisy: a few millimetres of depth noise, and
stray points floating in front of or behind the rock. Each 2 mm cell holds many
points, so taking any single point as "the deepest" turns noise into spikes,
and a mesh over spikes has many times the area of the rock. So stray points are
dropped first, each cell's depth is a high percentile of its points rather than
the maximum, and surface area is taken over a 3 x 3 median of those depths.

A phone only sees what its lens can reach. Deep, narrow crevices hide their
back walls, so every result carries `coverage`, the share of the mouth whose
interior was observed, and depth and volume are floors, never estimates of
what was not seen.
"""
from __future__ import annotations
import warnings
from dataclasses import asdict, dataclass
import cv2
import numpy as np
CELL_MM = 2.0
CELL_DEPTH_PERCENTILE = 90.0
SUPPORT_VOXEL_MM = 5.0
SUPPORT_SHARE = 0.05
MIN_HOLLOW_CM2 = 1.0
SHAPE_SIGMA_MM = 5.0
FACE_MAX_ANGLE_DEG = 60.0

def on_surface(points: np.ndarray, voxel_mm: float=SUPPORT_VOXEL_MM, share: float=SUPPORT_SHARE) -> np.ndarray:
    """Mask of the points that sit on a surface; isolated points and small loose clusters
    are False."""
    ...

def cell_percentile(cells: np.ndarray, values: np.ndarray, shape: tuple[int, int], percentile: float) -> np.ndarray:
    """Rows x cols: the percentile of `values` in each cell, NaN where a cell has none.
    `cells` holds (column, row) per value, all inside `shape`."""
    ...

def nan_median3(z: np.ndarray) -> np.ndarray:
    """3 x 3 median over the finite neighbours of each finite cell; NaN stays NaN."""
    ...

@dataclass
class Plane:
    origin: np.ndarray
    normal: np.ndarray

    def basis(self) -> tuple[np.ndarray, np.ndarray]:
        ...

    def to_local(self, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """(N x 2 in-plane coordinates, N depths; positive = into the rock)."""
        ...

@dataclass
class CreviceMetrics:
    opening_width_mm: float
    opening_height_mm: float
    depth_mm: float
    depth_p95_mm: float
    depth_mean_mm: float
    depth_median_mm: float
    mouth_area_cm2: float
    mouth_perimeter_mm: float
    volume_observed_ml: float
    surface_area_cm2: float
    rugosity: float
    coverage: float
    interior_points: int
    mouth_outline_mm: list
    rugosity_shape: float = 0.0
    rugosity_texture: float = 0.0
    depth_noise_mm: float = 0.0
    face_normal: list | None = None
    mouth_bounded: bool = True
    clipped_by: str | None = None

    def to_json(self) -> dict:
        ...

def fit_plane(points: np.ndarray, towards: np.ndarray) -> Plane:
    ...

def ransac_plane(points: np.ndarray, towards: np.ndarray, tolerance_mm: float=4.0, iterations: int=400, seed: int=0, facing: np.ndarray | None=None, max_angle_deg: float=FACE_MAX_ANGLE_DEG) -> Plane:
    """Dominant rock-face plane; the cavity itself is the outlier set.

    With `facing` (a unit vector towards the cameras), only planes within `max_angle_deg`
    of facing them are candidates, so a larger surface seen edge-on, like the floor below an
    overhang, is not taken for the face. If no plane qualifies, the dominant one is used."""
    ...

@dataclass
class DepthGrid:
    """The deepest observed surface behind the mouth, per CELL_MM cell of the mouth plane.

    `deepest` is NaN where nothing was seen; `mask` marks the cells inside the mouth.
    Cell (row j, column i) covers in-plane [lo + (i, j) * CELL_MM, lo + (i + 1, j + 1) * CELL_MM).
    """
    lo: np.ndarray
    mask: np.ndarray
    deepest: np.ndarray

    @property
    def seen(self) -> np.ndarray:
        ...

def depth_grid(local: np.ndarray, depth: np.ndarray, outline_2d: np.ndarray, margin_cells: int=1) -> DepthGrid:
    """Rasterise the mouth and keep the deepest point behind each cell of it."""
    ...

def surface_area_mm2(grid: DepthGrid, smooth_mm: float=0.0) -> float:
    """Area of the interior surface as seen through the mouth.

    The deepest surface of each seen cell and the rock at the mouth's edge (depth 0) are
    joined into a triangle mesh, so walls running straight back from the mouth count at
    their full height. Overhangs hidden behind the mouth, and cells nobody saw, do not count.
    Depths are median-filtered over 3 x 3 cells first, which keeps walls and steps but not
    one-cell spikes.
    """
    ...

def _nan_gaussian(z: np.ndarray, sigma_cells: float) -> np.ndarray:
    """Gaussian blur over the finite cells only; NaN stays NaN."""
    ...

def face_noise_mm(local: np.ndarray, depth: np.ndarray, outline: np.ndarray, ring_mm: float=16.0) -> float:
    """How noisy the cloud is: the robust scatter (1.4826 x median absolute deviation) of point
    depths about their cell's median, on the rock face in a ring just outside the mouth.

    Inside the mouth a cell at a wall holds every depth from the mouth to the back, so the face,
    where the rock crosses each cell as one surface, is where noise can be read."""
    ...

def measure_mouth(points: np.ndarray, plane: Plane, outline_2d: np.ndarray, extent_2d: np.ndarray | None=None) -> CreviceMetrics:
    """Measure a crevice given its mouth plane and outline in plane coordinates.

    `extent_2d` optionally gives in-plane points that bound the opening more
    tightly than the outline does (a rasterised outline overshoots the walls
    by up to a cell on a diagonal); width and height are taken from them."""
    ...

def _outline_3d(plane: Plane, outline_2d: np.ndarray) -> np.ndarray:
    ...

def measure_from_rim(points: np.ndarray, rim: np.ndarray, cameras: np.ndarray) -> CreviceMetrics:
    """The observer traced the mouth (at least three points, in order)."""
    ...

def measure_from_seed(points: np.ndarray, seed: np.ndarray, cameras: np.ndarray, radius_mm: float=200.0, min_depth_mm: float=8.0) -> CreviceMetrics:
    """Find the crevice nearest `seed` automatically. The seed can be on the rock round the
    opening or anywhere inside the crevice; the deepest part is the easiest to point at.

    Fits the rock face around the seed, marks everything more than
    `min_depth_mm` behind it as cavity, and takes the connected cavity region
    closest to the seed as the crevice. Its mouth is the hole in the rock face
    around that region, so a part the camera never saw into lowers coverage
    rather than the mouth's size.
    """
    ...

def mouth_behind(points: np.ndarray, near: np.ndarray, plane: Plane, seed: np.ndarray, radius_mm: float, min_depth_mm: float) -> CreviceMetrics:
    """The crevice behind `plane` nearest `seed`, from the points `near` it, measured on all `points`."""
    ...

def _reaches_scan_edge(region: np.ndarray, cells: np.ndarray) -> bool:
    """Whether the opening runs off the scanned rock: into empty cells joined to the edge of
    the grid, rather than being closed by rock all round. An unseen part inside the crevice is
    empty too, but walled in by the face."""
    ...

def _in_front(points: np.ndarray, plane: Plane, margin_mm: float=10.0) -> int:
    """How many points lie more than `margin_mm` in front of the plane, on the cameras' side."""
    ...

def towards_cameras(point: np.ndarray, cameras: np.ndarray) -> np.ndarray:
    """Unit vector from `point` towards the cameras: the mean of the directions to each."""
    ...

def camera_aim(centres: np.ndarray, forwards: np.ndarray) -> np.ndarray | None:
    """The point the cameras were aimed at: nearest, in least squares, to every viewing axis.

    A sweep keeps the crevice in the middle of the frame, so this lands in or near it. None
    when the axes are close to parallel and the point is poorly defined."""
    ...

def cube_placement(points: np.ndarray, face_normal: np.ndarray, outline: np.ndarray, edge_mm: float=40.0) -> dict:
    """Where the cube sat relative to the opening.

    The cube frame has its origin at the cube's centre and +Z out of the top face; the bottom
    face rests on the rock, or on a pole. Rock round the cube's base, level with its bottom,
    means it sat on a surface whose normal is the cube's +Z. That surface is compared with the
    face round the opening."""
    ...

def _with_unseen_mouth(region: np.ndarray, cells: np.ndarray, depth: np.ndarray, face_mm: float=4.0) -> np.ndarray:
    """Grow the cavity to the whole hole in the rock face around it.

    Parts of a crevice the camera never saw into have no deep points, so the cavity alone
    can cover only part of the mouth. The rock face is solid around the mouth, though, so
    the hole in it bounds the whole opening; the unseen part then counts against coverage
    instead of shrinking the mouth. Skipped when the hole leaks to the edge of the scan.
    """
    ...

def distance(a: np.ndarray, b: np.ndarray) -> float:
    """Straight-line distance, e.g. abalone shell length between two picked points."""
    ...

def _self_intersects(poly: np.ndarray) -> bool:
    ...

def _cross(p1, p2, q1, q2) -> bool:
    ...

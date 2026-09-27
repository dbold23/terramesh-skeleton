"""A textured mesh of the survey, in cube millimetres, and a USDZ of it to open on a phone.

OpenMVS meshes the dense cloud (ReconstructMesh) and paints it from the frames (TextureMesh).
Two choices here come from running it on field surveys:

- Seam levelling is off. In OpenMVS 2.4, TextureMesh's global and local seam levelling turn
  most patches black; without it the patches keep their own colours, and seams show as slight
  steps in brightness.
- TextureMesh writes PLY. Its OBJ export crashes in 2.3, and PLY carries the same thing: per-face
  texture coordinates and one PNG per texture page.

The mesh comes out in the SfM model's frame and is moved into cube millimetres with the cube
similarity, like the dense cloud. The USDZ is in metres with +Y up. Up is gravity from ARKit
when the survey has ARKit poses, and otherwise the cube's +Z. The origin is the crevice's mouth
when one was measured. It is a lighter copy (`for_phone`): the whole scan with fewer
triangles and one packed texture, so it opens in AR Quick Look on an iPhone. USDZ writing needs usd-core
(`pip install usd-core`, the `mesh` extra); without it only the PLY and PNG are written.
"""
from __future__ import annotations
import shutil
from pathlib import Path
import cv2
import numpy as np
from . import dense
from .scale import Similarity

def find(bin_dir: Path) -> Path:
    ...

def build(work: Path, bin_dir: Path, max_faces: int=1500000, texture_size: int=8192, log=None) -> Path:
    """Mesh and texture the dense scene that `dense.densify` left in `work`. Returns the textured
    PLY, in the SfM model's frame, with its PNG pages beside it."""
    ...

class Mesh:
    """Triangles with per-corner texture coordinates on one or more texture pages."""

    def __init__(self, vertices: np.ndarray, faces: np.ndarray, uv: np.ndarray, page: np.ndarray, textures: list[str]):
        ...

def read(path: Path) -> Mesh:
    """TextureMesh's binary PLY: triangles, six texture coordinates per face, and a page number
    per face when there is more than one texture."""
    ...

def write(path: Path, mesh: Mesh) -> None:
    """Binary PLY in TextureMesh's own layout, which MeshLab and Blender read with textures."""
    ...

def to_cube(textured: Path, transform: Similarity, out_dir: Path, name: str='mesh-mm') -> Path:
    """The textured mesh in cube millimetres, as out_dir/name.ply with its texture pages."""
    ...

def upright(up: np.ndarray) -> np.ndarray:
    """Rotation taking `up` (cube frame) to +Y, turning as little as possible."""
    ...

def crop(mesh: Mesh, centre: np.ndarray, radius: float) -> Mesh:
    """The faces whose centroids lie within `radius` of `centre`."""
    ...

def _cluster(mesh: Mesh, cell: float) -> Mesh:
    ...

def decimate(mesh: Mesh, max_faces: int) -> Mesh:
    """At most `max_faces` triangles, by merging the vertices in each cell of a grid (vertex
    clustering). Each kept face keeps its own texture coordinates, so the picture moves by at
    most about a cell on the surface: a millimetre or two at the default sizes."""
    ...

def _pack(sizes: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], int, int]:
    """Shelf packing: where each (w, h) rectangle goes, tallest first, and the atlas size."""
    ...

def atlas(mesh: Mesh, texture_dir: Path, max_size: int=4096, pad: int=2, repacked: bool=False) -> tuple[Mesh, np.ndarray]:
    """One texture holding only the parts of the pages that `mesh`'s faces use, packed tight
    and scaled to at most `max_size` pixels a side. TextureMesh's own pages are mostly empty
    space, and after a crop more so."""
    ...

def for_phone(mesh_ply: Path, centre: np.ndarray, radius_mm: float | None=None, max_faces: int=250000, max_texture: int=4096) -> tuple[Mesh, np.ndarray]:
    """The whole scanned mesh, or with `radius_mm` only the part within it of `centre` (cube mm),
    light enough for AR Quick Look: at most `max_faces` triangles and one texture of at most
    `max_texture` pixels a side. The full-resolution mesh stays in the PLY for measuring."""
    ...

def usdz(mesh: Mesh, picture: np.ndarray, path: Path, up: np.ndarray, origin: np.ndarray, jpeg_quality: int=85) -> Path:
    """Write `mesh` (cube mm, one texture) as a USDZ in metres, +Y up, with `origin` (cube mm) at zero."""
    ...

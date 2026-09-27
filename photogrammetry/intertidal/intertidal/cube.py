"""The calibration cubes, and the scale bar, as the scale solver sees them: tag ids and metric corners.

One `Cube` can hold several rigid tag sets: printed cubes, and the scale bar (two plates on a
steel rule, hardware/scale-bar). Each keeps its own frame (its corners are in millimetres about
its own origin) and `cube_of` says which set a tag is on, so the solver can fit one shared
scale with a separate pose per set. The bar is set `SCALE_BAR_GROUP`; its 882 mm baseline sets
the scale about ten times better than a 40 mm cube, so the solver checks the cubes against it.

Tag ids must be unique across everything in view. The 120 mm field cube on main uses tag36h11
ids 0-5, the same as cubes 0 and 1 here: never film them together (`FIELD_CUBE_IDS`)."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
SCALE_BAR_GROUP = 100

def spec_paths(folder: Path=CUBE_FOLDER) -> list[Path]:
    """Every cube spec in a folder: cube-spec.json (cube 0) and cube-spec-<n>.json."""
    ...

@dataclass(frozen=True)
class Cube:
    edge_mm: float
    tag_mm: float
    corners: dict[int, np.ndarray]
    normals: dict[int, np.ndarray]

    def cube_index(self, tag_id: int) -> int:
        ...

    def tag_mm_of(self, tag_id: int) -> float:
        ...

    @staticmethod
    def is_bar(index: int) -> bool:
        ...

    @staticmethod
    def name(index: int) -> str:
        ...

    @property
    def cubes(self) -> list[int]:
        ...

    @classmethod
    def load(cls, path: Path=DEFAULT_SPEC, measured_tag_mm: float | None=None, measured_edge_mm: float | None=None) -> 'Cube':
        """Load cube-spec.json.

        `measured_tag_mm` is the tag edge as measured on the printed cube with
        calipers. FDM prints are typically off by 0.1 to 0.3 mm, which is up to 1%
        of a 32 mm tag, so a measured value beats the nominal one whenever it exists.
        Tags are scaled about their own centres; the cube edge is left alone.

        `measured_edge_mm` is the cube measured with calipers across opposite tagged
        faces (the mean of the readings). The fit uses the distances between faces as
        well as the tag sizes, so a tile that sits proud or a print that came out large
        would bias the scale; each tag is moved along its face normal to match.
        """
        ...

    @classmethod
    def load_bar(cls, path: Path=SCALE_BAR_SPEC) -> 'Cube':
        """The scale bar: four tags on two plates, in one rigid frame whose length comes from the
        steel rule's graduations (the spec's `baseline_mm`). Caliper readings of a cube do not
        apply to it."""
        ...

    @classmethod
    def load_many(cls, paths: list[Path], measured_tag_mm: float | None=None, measured_edge_mm: float | None=None) -> 'Cube':
        """Several printed cubes at once (a long crevice, a shark on a deck), and the scale bar
        when its spec is among `paths`. The cubes must share the cube size; the caliper readings
        apply to all of them, as they come off the same printer."""
        ...

    @property
    def ids(self) -> list[int]:
        ...

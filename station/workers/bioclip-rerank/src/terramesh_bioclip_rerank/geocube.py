"""The TMGC occurrence cube: species × grid cell × month record counts, and the presence score
read from it.

The phone (TerraMeshCore `SpeciesOccurrenceCube`) reads the same file with the same arithmetic,
so any change here is a format change: bump `VERSION`, update the Swift reader, and regenerate the
golden fixture both test suites share (`tests/test_geocube.py::GOLDEN`).

File layout, all little-endian:

    offset  type      field
    0       4 bytes   magic "TMGC"
    4       u32       version (1)
    8       u32       taxon count
    12      u32       cell count
    16      f64       cell size in degrees (180 and 360 are whole multiples of it)
    24      f32       saturation: records at which presence reaches 1 - 1/e
    28      f32       all-year weight added to every month
    32      f32       weight of each adjacent month
    36      u32       minimum weighted effort before the cube says anything
    40      u32       neighbourhood radius in cells
    44      u32       meta JSON length in bytes
    48      f32       presence given to a vocabulary taxon the source never named
    52      12 bytes  reserved, zero
    64      meta JSON (UTF-8), zero-padded to a multiple of 4
    then    cells, 64 bytes each, sorted by (row, col):
              u32 row, u32 col, u32 first entry, u32 entry count, 12 × u32 records per month (all taxa)
    then    entries, 16 bytes each, grouped by cell and sorted by taxon:
              u32 taxon index, 12 × u8 records per month, capped at 255

row = floor((latitude + 90) / cell size) and col = floor((longitude + 180) / cell size), with
columns wrapping at the antimeridian. Counts are capped at 255 because presence has long since
saturated by then; the per-cell totals, which measure sampling effort, are not capped.
"""
from __future__ import annotations
import bisect
import json
import math
import struct
from dataclasses import dataclass, field
from pathlib import Path
VERSION = 1
MINIMUM_GEO_SCORE = 0.005

@dataclass(frozen=True)
class ScoringConstants:
    saturation: float = 3.0
    all_year_weight: float = 0.1
    adjacent_month_weight: float = 0.5
    minimum_effort: int = 200
    radius_cells: int = 2
    unmatched_presence: float = 0.0

@dataclass
class OccurrenceCube:
    cell_degrees: float
    constants: ScoringConstants
    meta: dict
    taxon_count: int

    @property
    def rows(self) -> int:
        ...

    @property
    def cols(self) -> int:
        ...

    @property
    def taxa(self) -> list[dict]:
        ...

    def cell_index(self, latitude: float, longitude: float) -> tuple[int, int] | None:
        ...

    def _cell(self, row: int, col: int) -> int | None:
        ...

    def month_weights(self, month: int) -> list[float]:
        ...

    def weighted_counts(self, latitude: float, longitude: float, month: int) -> tuple[list[float], float] | None:
        """Neighbourhood- and season-weighted records per taxon, and the same weighting of all
        records (the effort). None for an impossible place or month."""
        ...

    def presence(self, latitude: float, longitude: float, month: int) -> list[float] | None:
        """One presence score in [0, 1) per taxon, in cube order.

        None means the cube has nothing to say here: the place is impossible, or too few records
        of anything were made nearby for an absence to mean anything. The caller must then rank on
        vision alone, because an unsurveyed place is not evidence that a species is missing.
        """
        ...

def combine(vision: list[float], geo: list[float]) -> list[float] | None:
    """`SpeciesGeoPrior.combine`: floor the prior, multiply, renormalise. None when unusable."""
    ...

def solar_month(epoch_milliseconds: float, longitude: float) -> int:
    """Calendar month at the place, from UTC shifted by longitude / 15 hours.

    The export carries no time zone. Mean solar time is never more than about an hour from civil
    time, which only matters in the last hour of a month, and it is the same rule the phone uses.
    """
    ...

class CubeFormatError(ValueError):
    ...

def read(path: Path) -> OccurrenceCube:
    ...

def parse(data: bytes) -> OccurrenceCube:
    ...

def serialise(*, cell_degrees: float, constants: ScoringConstants, meta: dict, taxon_count: int, cells: dict[tuple[int, int], tuple[list[int], dict[int, list[int]]]]) -> bytes:
    """`cells` maps (row, col) to (12 monthly totals, {taxon: 12 monthly counts})."""
    ...

def _padded(length: int) -> int:
    ...

def _whole(value: float) -> bool:
    ...

"""Readers for a phone survey export (directory or ZIP), streamed.

The export is written by ``SurveyStore.exportSurvey``.  Its JSON comes from a
``JSONEncoder`` with ``.sortedKeys`` and **no** key strategy, so every key is the
Swift property name verbatim in camelCase, nil optionals are *omitted* rather
than written as null, and dates are floating-point **milliseconds since the Unix
epoch** — except ``FrameRecord.timestamp``, ``RoutePoint.timestamp`` and the
coverage snapshots' ``startedAt``/``endedAt``, which are monotonic ARKit stream
*seconds*.  ``earth-placement.json`` is the one file built with
``JSONSerialization``: its top-level keys are snake_case while the embedded
``alignment`` object stays camelCase.

Nothing here reads a whole journal into memory, and nothing here writes into the
export.  A trailing partial line is expected in these crash-tolerant journals and
is skipped rather than raised.
"""
from __future__ import annotations
import hashlib
import io
import json
import os
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
import numpy as np

def ms_to_iso(value):
    """Milliseconds since the epoch -> ISO-8601 UTC, or None."""
    ...

def ms_to_date(value):
    """Milliseconds since the epoch -> 'YYYY-MM-DD' (UTC), or None."""
    ...

def column_major_to_matrix(values):
    """A flat 16 (column-major) -> 4x4 row-major numpy matrix."""
    ...

def matrix_to_column_major(matrix):
    ...

def intrinsics_from_flat(values):
    """A flat 9 (column-major 3x3) -> (fx, fy, cx, cy)."""
    ...

def vector3(value):
    """``{"x":…,"y":…,"z":…}`` -> ``[x, y, z]``, or None."""
    ...

class Source:
    """A survey export, read-only, whether it is a directory or a ZIP."""

    def names(self) -> list:
        ...

    def exists(self, name: str) -> bool:
        ...

    def open(self, name: str):
        ...

    def size(self, name: str) -> int:
        ...

    def read_json(self, name: str):
        ...

    def iter_jsonl(self, name: str):
        """Stream one record per line, skipping blank or truncated trailing lines."""
        ...

    def sha256(self, name: str) -> str:
        ...

    def copy_to(self, name: str, destination: str) -> str:
        ...

class DirSource(Source):

    def __init__(self, root):
        ...

    def names(self) -> list:
        ...

    def exists(self, name: str) -> bool:
        ...

    def open(self, name: str):
        ...

    def size(self, name: str) -> int:
        ...

class ZipSource(Source):
    """Reads an export ZIP in place.  Nothing is ever extracted into the source tree."""

    def __init__(self, path):
        ...

    def names(self) -> list:
        ...

    def exists(self, name: str) -> bool:
        ...

    def open(self, name: str):
        ...

    def size(self, name: str) -> int:
        ...

    def close(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, *exc):
        ...

def open_source(path) -> Source:
    ...

@dataclass
class Frame:
    id: str
    timestamp: float
    captured_at: str | None
    segment_id: str | None
    camera_to_world: np.ndarray
    fx: float | None
    fy: float | None
    cx: float | None
    cy: float | None
    width: int
    height: int
    tracking_state: str | None
    capture_reason: str | None
    image_path: str | None
    feature_point_count: int | None = None

    @property
    def centre(self) -> np.ndarray:
        ...

    @property
    def is_normal(self) -> bool:
        ...

    @property
    def image_name(self) -> str:
        ...

def iter_frames(source: Source, name: str='frames.jsonl'):
    """Stream ``frames.jsonl`` as :class:`Frame` records."""
    ...

def iter_locations(source: Source, name: str='locations.jsonl'):
    """Stream ``locations.jsonl``; timestamps become ISO-8601."""
    ...

def iter_sparse_points(source: Source, name: str='sparse-points.jsonl'):
    """Stream ``sparse-points.jsonl`` records as-is (camelCase keys preserved)."""
    ...

def iter_measurements(source: Source, name: str='measurements.jsonl'):
    """Stream ``measurements.jsonl`` as snake_case records; last line per id wins upstream."""
    ...

def measurement_record(record: dict) -> dict:
    """One ``ObservationMeasurement`` in the package's snake_case spelling, verbatim values."""
    ...

def read_encounter(source: Source) -> dict | None:
    """The guided encounter's summary, in the package's snake_case spelling.

    A view is listed only because the operator confirmed it on a frame that cleared the
    stated image gates. ``accepted`` is how many such confirmations there were; a view with
    ``confirmed`` true and ``accepted`` zero was confirmed and then failed a gate, which is
    recorded rather than discarded. ``classifier_agreed`` is what an optional trained view
    head thought, and it is never what completed the row.
    """
    ...

def iter_arc_stills(source: Source, name: str=ENCOUNTER_ARC_STILLS):
    """Stream the arc-still index as snake_case records.

    ``azimuth_degrees`` is measured around a rough subject centre taken from the depth map,
    so it describes the operator's walk around the animal and not the animal's geometry.
    """
    ...

def iter_clips(source: Source, name: str='clips.jsonl'):
    """Stream ``clips.jsonl`` as snake_case records with the media path attached."""
    ...

def read_joins(source: Source, name: str='joins.json') -> list:
    """``joins.json`` -> ``JoinedContext`` records in snake_case, values verbatim."""
    ...

def _identification(value):
    ...

def _contact_hazard(evidence_list):
    """The strongest contact-hazard reading among an observation's evidence, if any."""
    ...

def read_observations(source: Source, manifest: dict | None=None) -> list:
    """``manifest.json`` observations in the package's shape.

    Field mapping (export -> package): ``createdAt`` ms -> ISO ``created_at``,
    ``segmentID`` -> ``segment_id``, ``geometricResidual`` -> ``geometric_residual_m``,
    ``lifeState`` -> ``life_state``, ``catalogRole`` -> ``catalog_role``,
    ``reviewStatus``/``verification`` -> ``export_prior`` (read-only), and each
    ``evidence`` entry's ``imagePath``/``pixelX``/``pixelY``/``depthMetres`` ->
    ``image``/``pixel_x``/``pixel_y``/``depth_m``.  ``contact_hazard`` is folded
    from ``evidence[].sceneDescription.contactHazard*``; the export has no
    observation-level field for it.
    """
    ...

def read_segments(manifest: dict) -> list:
    """Segments as the package records them.  A segment carries no coordinate of its
    own; geographic reference lives in ``geographicAlignments``, keyed by segmentID."""
    ...

def read_earth_placement(source: Source, name: str='earth-placement.json'):
    """``earth-placement.json`` -> ``{segment_id: {...}}``; snake_case top level.

    Each entry keeps the raw ``local_to_enu_column_major``, the segment's own
    ``referenceCoordinate`` (which is where that matrix's ENU origin sits) and the
    alignment's own accuracy numbers.  ``global_altitude`` is always null by design.
    """
    ...

def read_coverage_policy(source: Source, name: str='coverage.json'):
    """Cell size and elevation band from the newest coverage snapshot.

    Returns ``(cell_size_m, elevation_band_m, caveat_or_None)``.  When
    ``coverage.json`` is absent the policy defaults (0.5 m, 1.0 m) are used and a
    caveat says so, because a survey recorded under a different policy would put
    the patches on a different grid.
    """
    ...

def read_realitykit_poses(path):
    """RealityKit ``poses.json`` -> ``{file name: (centre, camera_to_world 4x4)}``.

    Translation plus ``rotationQuaternionXYZW``; the frame is RealityKit's own
    estimated local frame, Y up, with a scale nothing has verified.
    """
    ...

def coverage_patches(records) -> list:
    """Fold ``sparse-points.jsonl`` records into coverage patches.

    Dedup key is ``(segmentID, identifier)`` with the highest ``revision`` winning,
    exactly as the phone folds them.  Only the surviving revision of each track
    contributes to a patch.
    """
    ...

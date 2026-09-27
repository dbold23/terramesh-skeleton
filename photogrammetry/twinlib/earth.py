"""WGS84 local tangent plane, ported from TerraMeshCore.

Port of ``GeographicAlignment.swift`` (``WGS84.xyz`` and ``WGS84.eastNorth``,
lines 272-291).  The port is deliberately literal: the same ellipsoid constants,
the same chord guard, the same two-term tangent projection, so a Python
re-basing and the phone's own placement agree to floating point.

Heights are never produced here.  ``earth-placement.json`` gives each segment an
affine local-to-ENU matrix expressed at *that segment's* reference coordinate
(``SurveyStore.swift:1244``); the vertical offset between two segments'
references is not observed by anything in the export, so ``rebase_segment``
returns ``None`` for it and the caller records ``vertical_state: "unresolved"``.
"""
from __future__ import annotations
import math
import numpy as np
A = 6378137.0
E2 = 0.0066943799901413165
MAXIMUM_EXTENT_METRES = 20000.0

class OutOfRange(ValueError):
    """The two coordinates are further apart than the tangent plane is valid for."""

def is_valid(latitude, longitude) -> bool:
    """Mirror of ``GeographicCoordinate.isValid``."""
    ...

def wrap_longitude(value: float) -> float:
    ...

def ecef(latitude: float, longitude: float):
    """Geocentric XYZ on the reference ellipsoid; altitude is deliberately omitted."""
    ...

def east_north(latitude, longitude, ref_latitude, ref_longitude):
    """Metres east and north of the reference, on the WGS84 tangent plane.

    Returns ``None`` when either coordinate is invalid or the chord exceeds the
    20 km validity limit, exactly as the Swift original returns ``nil``.
    """
    ...

def coordinate(east: float, north: float, ref_latitude: float, ref_longitude: float):
    """Inverse of :func:`east_north`; horizontal only, as in the Swift original."""
    ...

def _to_matrix(column_major) -> np.ndarray:
    ...

def _to_column_major(matrix: np.ndarray) -> list:
    ...

def rebase_segment(local_to_enu_column_major, segment_ref_latlon, site_anchor_latlon):
    """Re-base one segment's ENU placement onto the site anchor's ENU frame.

    ``local_to_enu_column_major`` maps that segment's local metres to ENU metres
    at ``segment_ref_latlon``.  The site frame is ENU at ``site_anchor_latlon``.
    The two ENU frames differ by a horizontal translation (their axes are
    parallel to within a few arcseconds over the 20 km the tangent plane covers)
    and by an unknown vertical offset.

    Returns ``(matrix_column_major, up_offset)`` where ``up_offset`` is always
    ``None``: nothing in the export observes the height difference between two
    segments' reference positions, so vertical deltas across segments are
    unsupported and the caller must record ``vertical_state: "unresolved"``.
    """
    ...

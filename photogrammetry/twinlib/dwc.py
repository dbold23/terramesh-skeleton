"""Darwin Core Archive mapping for TerraMesh twin packages.

This module turns a twin package (``twinlib/SCHEMA.md``, format 1) into a
GBIF-style **sampling-event** Darwin Core Archive: an Event core with
Occurrence, ExtendedMeasurementOrFact and Simple Multimedia extensions.

It is deliberately self-contained.  Nothing here imports another ``twinlib``
module, so the exporter runs against a package built by any version of the
builder: the JSON and JSONL readers, the WGS84 tangent-plane inverse and the
convex hull are all local.  The WGS84 inverse is a literal port of
``WGS84.coordinate(east:north:reference:)`` in
``ios/TerraMeshCore/Sources/TerraMeshCore/GeographicAlignment.swift`` (lines
290-300), with the same ellipsoid constants, so a coordinate exported here and
the same coordinate computed on the phone agree to floating point.

The mapping never promotes a claim.  A coordinate is written only when the
package actually carries one: the site frame must be ``enu_metric``, the
observation's layer must have a ``registered`` or ``declared`` transform to the
site frame, and the observation must have a non-null position that is not
``pending``.  Anything else leaves ``decimalLatitude``/``decimalLongitude``
empty and says why in ``georeferenceRemarks``.  ``organismID`` is never
emitted, because nothing in a twin package asserts individual identity --
temporal-track tags say so themselves (``identity_claim: "none"``).
"""
from __future__ import annotations
import io
import json
import math
import os
import zipfile
from datetime import datetime, timezone
A = 6378137.0
E2 = 0.0066943799901413165
MAXIMUM_EXTENT_METRES = 20000.0

def is_valid(latitude, longitude) -> bool:
    """Mirror of ``GeographicCoordinate.isValid``."""
    ...

def wrap_longitude(value: float) -> float:
    ...

def ecef(latitude: float, longitude: float):
    """Geocentric XYZ on the reference ellipsoid; altitude is deliberately omitted."""
    ...

def east_north(latitude, longitude, ref_latitude, ref_longitude):
    """Metres east and north of the reference, on the WGS84 tangent plane."""
    ...

def coordinate(east, north, ref_latitude, ref_longitude):
    """Inverse of :func:`east_north`: ENU metres -> (latitude, longitude).

    Literal port of ``WGS84.coordinate(east:north:reference:)``.  Returns
    ``None`` on the same conditions the Swift original returns ``nil``: an
    invalid reference, a non-finite offset, or an offset beyond the 20 km the
    tangent plane is valid for.  Height is never produced.
    """
    ...

def read_json(path):
    ...

def read_json_or_none(path):
    ...

def iter_jsonl(path):
    """Stream a journal one record per line; blank and unparsable lines are skipped."""
    ...

def latest_by_id(path):
    """Last revision per id wins, as the journals specify.  Streams the file."""
    ...

def transform_point(matrix_column_major, point):
    """Apply a column-major 4x4 to a 3-vector: ``[x', y', z', 1] = M . [x, y, z, 1]``."""
    ...

def convex_hull(points):
    """Monotone chain hull of (x, y) pairs; returns the hull in counter-clockwise order."""
    ...

def polygon_wkt(lonlat):
    """POLYGON WKT in EPSG:4326 axis order as GBIF reads it: longitude first."""
    ...

class Package:
    """A loaded twin package: manifests, transforms, journals and per-visit layers."""

    def __init__(self, root):
        ...

    def _read_audit(self):
        """Author per visit (and for the package) plus the review fold, in one pass."""
        ...

    def author_for(self, visit_id):
        ...

    def visit_json(self, visit_id):
        ...

    def layer_id(self, visit_id, kind):
        ...

    def layer_path(self, visit_id, kind, *parts):
        ...

    def layer_file(self, visit_id, kind, name):
        ...

    def transform_for_layer(self, visit_id, kind):
        """The transform that carries a layer to the site frame.

        A layer whose ``frame_id`` names another layer shares that layer's
        transform, so the frame reference is followed (with a cycle guard)
        before the transform table is consulted.
        """
        ...

    @property
    def is_enu(self):
        ...

    @property
    def anchor_latlon(self):
        ...

    def site_to_latlon(self, site_position):
        """Site-frame ENU metres -> (latitude, longitude), or None."""
        ...

    def layer_point_to_site(self, visit_id, kind, position):
        """Layer-frame point -> site-frame point, when the transform supports it."""
        ...

def transform_uncertainty(transform):
    ...

def ceil_to_decimetre(value):
    """Round a metre uncertainty up to the next 0.1 m, never below 0.1 m."""
    ...

def combine_uncertainty(*components):
    ...

def number(value, digits=None):
    ...

def text(value):
    ...

def json_field(payload):
    ...

def iso_day(value):
    ...

def vitality_of(life_state):
    ...

def verification_author(verification):
    ...

def verification_date(verification):
    ...

class Archive:
    """The four tables, plus the options that describe the dataset."""

    def __init__(self, options):
        ...

    def table(self, name):
        ...

class Options:

    def __init__(self, dataset_name='', rights_holder='', creator='', license_id='', visits=None):
        ...

def _station_positions(package, visit_id):
    """Station translations in the site frame, when the stations layer is placed."""
    ...

def _station_times(package, visit_id):
    ...

def _footprint(package, site_positions):
    ...

def _visit_dates(package, visit_id):
    """(eventDate, started, ended): the survey interval when segments carry one."""
    ...

def _sampling_protocol(package, visit_id):
    ...

def _gps_accuracy(package, visit_id):
    """Typical GPS accuracy per segment id, from the visit's earth placements."""
    ...

def build_events(package, visit_ids, archive):
    """One row per visit plus the site-level parent event."""
    ...

def _track_ids(package, anchor_ids):
    """Temporal-track tags whose members include any of these anchors."""
    ...

def _anchors_by_observation(package):
    ...

def _identification_columns(package, observation):
    """basisOfRecord and the identification block, honestly derived."""
    ...

def _coordinates(package, visit_id, observation, gps_accuracy):
    """Coordinates and their uncertainty, or the reason there are none."""
    ...

def build_occurrences(package, visit_ids, archive, anchors_by_observation):
    ...

def build_measurements(package, visit_ids, archive):
    ...

def build_archive(package, options):
    ...

def clean(value):
    """Tabs and newlines would break a field; nothing else is altered."""
    ...

def write_table(path, fields, rows):
    ...

def meta_xml(tables):
    """``meta.xml`` with the full term URIs; ``tables`` is the FILES layout."""
    ...

def escape_xml(value):
    ...

def eml_xml(package, options, counts):
    ...

def write_archive(out_dir, package, archive, zip_path=None):
    """Write the four tables, ``meta.xml`` and ``eml.xml``, then zip the folder."""
    ...

def read_table(path):
    ...

def parse_meta(path):
    """Enough of ``meta.xml`` to check it against the tables: file -> term names."""
    ...

def validate_archive(out_dir):
    """Structural read-back of a written archive.  Returns a list of problems."""
    ...

def export(package_root, out_dir, options, validate=False):
    """Load, map, write, optionally read back.  Returns (counts, problems, zip path)."""
    ...

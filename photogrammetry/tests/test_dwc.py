"""Darwin Core Archive export: mapping, honesty and read-back.

The fixture is a minimal twin package written to a tmp directory following
``twinlib/SCHEMA.md``: an ENU site anchored at 36.6, -121.9, one visit, four
observations (placed + machine-identified, placed + human-confirmed, pending,
dead), two measurements (one unsupported), one joined context, two anchors and
one temporal-track tag carrying a taxon.
"""
from __future__ import annotations
import csv
import json
import math
import os
import sys
import pytest
import export_dwc
from twinlib import dwc
ANCHOR_LAT, ANCHOR_LON = (36.6, -121.9)

def write_json(path, payload):
    ...

def write_jsonl(path, records):
    ...

def observations():
    ...

def build_package(root, frame_kind='enu_metric'):
    """Write a minimal but schema-shaped twin package under ``root``."""
    ...

def read_table(path):
    ...

@pytest.fixture(scope='module')
def exported(tmp_path_factory):
    ...

def by_id(rows, key='occurrenceID'):
    ...

@pytest.mark.parametrize('east,north', [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (123.4, -56.7), (-2000.0, 3500.0)])
def test_enu_inverse_round_trips(east, north):
    ...

def test_out_of_range_offsets_have_no_coordinate():
    ...

def test_row_counts(exported):
    ...

def test_event_rows(exported):
    ...

def test_basis_of_record_per_row(exported):
    ...

def test_unidentified_observations_say_so(exported):
    ...

def test_pending_observation_has_no_coordinates(exported):
    ...

def test_placed_observation_coordinates(exported):
    ...

def test_every_coordinate_carries_an_uncertainty(exported):
    ...

def test_organism_id_is_never_emitted(exported):
    ...

def test_vitality_and_remarks(exported):
    ...

def test_dynamic_properties(exported):
    ...

def test_standalone_anchor_becomes_an_occurrence(exported):
    ...

def test_associated_media_and_multimedia(exported):
    ...

def test_measurement_rows(exported):
    ...

def test_unsupported_measurement_has_no_value(exported):
    ...

def test_hazard_and_join_rows(exported):
    ...

def test_validate_passes(exported):
    ...

def test_meta_and_eml(exported):
    ...

def test_tables_are_tab_separated_with_one_header(exported):
    ...

def test_local_unscaled_site_produces_no_coordinates(tmp_path):
    ...

def test_cli_round_trip(tmp_path, capsys):
    ...

def test_cli_visit_filter_and_unknown_visit(tmp_path):
    ...

def test_validate_catches_a_broken_archive(exported, tmp_path):
    ...

def test_site_named_after_its_only_visit_keeps_a_distinct_parent_event(tmp_path):
    """A one-visit package often names the visit after the site (curb-02 does)."""
    ...

def test_unreviewed_is_not_a_human_confirmation(tmp_path):
    """`export_prior.review_status == "unreviewed"` says nobody reviewed the record."""
    ...

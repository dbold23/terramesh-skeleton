"""The guided encounter in the twin package and in the Darwin Core archive.

What these tests hold the code to: a confirmed view is a human statement about one photograph
that also cleared the stated image gates, and every row that leaves the package says so. A view
the operator confirmed and the gates rejected must survive as a zero with its reason, not vanish;
a trained view head's opinion must be recorded beside the human's and never in place of it; and
the arc stills must be counted without any claim that a reconstruction succeeded.
"""
from __future__ import annotations
import csv
import json
import os
import sys
import pytest
import build_twin
import export_dwc
from twinlib import arkit, dwc
from tests.test_dwc import VISIT, build_package, write_json, write_jsonl

def test_read_encounter_maps_to_snake_case_without_inventing_anything(tmp_path):
    ...

def test_a_walked_export_has_no_encounter(tmp_path):
    ...

@pytest.fixture(scope='module')
def encounter_archive(tmp_path_factory):
    """A twin package whose observations layer carries an encounter, exported to DwC."""
    ...

def _summary_source(tmp_path_factory):
    ...

def _rows(archive, prefix):
    ...

def test_one_emof_row_per_confirmed_view(encounter_archive):
    ...

def test_a_view_the_gates_rejected_is_a_zero_with_its_reason(encounter_archive):
    ...

def test_the_view_head_is_recorded_beside_the_human_never_instead_of_one(encounter_archive):
    ...

def test_every_view_row_refuses_to_imply_an_identification(encounter_archive):
    ...

def test_handling_duration_and_arc_stills_are_their_own_rows(encounter_archive):
    ...

def test_the_encounter_rows_survive_a_written_archive(tmp_path):
    ...

def test_a_package_without_an_encounter_emits_no_encounter_rows(tmp_path):
    ...

def test_encounter_visit_ids_resolves_paths_and_bare_ids():
    ...

def test_the_mesh_step_declines_rather_than_inventing_geometry(tmp_path, capsys):
    """Every reason Object Capture cannot run leaves the arc index intact and adds no layer."""
    ...

class _visit:

    def __init__(self, identifier):
        ...

import base64
import json
import math
from pathlib import Path
import pytest
from terramesh_bioclip_rerank import geocube
from terramesh_bioclip_rerank.geocube_build import build

def golden_cube() -> bytes:
    """A 1° cube around Monterey Bay with three taxa. The Swift tests read the same bytes."""
    ...

def hand_presence(counts, effort_ok=True):
    ...

def test_round_trip_and_hand_computed_presence():
    ...

def test_too_little_effort_says_nothing():
    ...

def test_columns_wrap_at_the_antimeridian():
    ...

def test_combine_matches_swift_species_geo_prior():
    ...

def test_solar_month_uses_longitude():
    ...

def test_rejects_bad_files():
    ...

def test_golden_fixture_is_current():
    """The Swift tests embed this fixture. Regenerate with `python tests/test_geocube.py`."""
    ...

def golden_fixture() -> dict:
    ...

def test_build_counts_every_record_as_effort():
    ...

def test_bank_cube_matches_synonyms_and_never_favours_out_of_range_names():
    ...

def test_binomial_reads_authorship_and_rejects_non_binomials():
    ...

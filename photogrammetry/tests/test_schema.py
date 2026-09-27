"""The validators, and in particular the rules that keep the package honest."""
import json
import os
import shutil
import tempfile
import unittest
from tests.support import PHOTOGRAMMETRY, SYNTHETIC_PACKAGE
from twinlib import audit, schema
import register_twin

def anchor(**overrides):
    ...

def tag(**overrides):
    ...

class TestAnchorRules(unittest.TestCase):

    def test_a_valid_anchor_passes(self):
        ...

    def test_site_position_is_refused_on_an_unregistered_anchor(self):
        ...

    def test_site_position_is_refused_on_a_declared_anchor(self):
        ...

    def test_a_null_site_position_is_fine_at_any_state(self):
        ...

    def test_a_bad_kind_is_refused(self):
        ...

    def test_a_barycentric_anchor_needs_its_block(self):
        ...

class TestTagRules(unittest.TestCase):

    def test_a_valid_tag_passes(self):
        ...

    def test_identity_claim_must_be_none(self):
        ...

    def test_an_unknown_match_method_is_refused(self):
        ...

class TestTransformRules(unittest.TestCase):

    def registered(self, **overrides):
        ...

    def test_a_valid_registered_transform_passes(self):
        ...

    def test_registered_with_a_null_rmse_is_refused(self):
        ...

    def test_registered_with_no_matrix_is_refused(self):
        ...

    def test_unregistered_must_carry_a_reason_and_no_matrix(self):
        ...

    def test_identity_pin_must_be_declared_and_the_identity(self):
        ...

    def test_an_unknown_scale_source_is_refused(self):
        ...

    def test_realitykit_similarity_is_an_accepted_scale_source(self):
        ...

    def test_to_frame_must_be_the_site(self):
        ...

class TestEventRules(unittest.TestCase):

    def test_a_valid_event_passes(self):
        ...

    def test_seq_zero_needs_the_zero_hash(self):
        ...

    def test_an_unknown_agent_is_refused(self):
        ...

class TestUnknownKind(unittest.TestCase):

    def test_validate_record_refuses_an_unknown_kind(self):
        ...

class TestAuditGrowthIsANote(unittest.TestCase):
    """`twin.json.integrity` is what the chain looked like when the builder wrote it.

    The viewer appends to `audit.jsonl` through `twin-viewer/serve.py` and never
    rewrites the manifest, so the first tag anybody creates puts the journal ahead of
    the snapshot.  That has to stay valid, or every package becomes invalid the first
    time it is used.  What must stay a failure is a journal that was rewritten rather
    than appended to.
    """

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def _manifest(self):
        ...

    def _append_viewer_event(self):
        ...

    def test_the_untouched_package_validates_with_no_notes(self):
        ...

    def test_a_grown_journal_is_a_note_and_not_a_problem(self):
        ...

    def test_notes_are_optional_and_never_change_the_result(self):
        ...

    def test_the_manifest_head_must_still_be_the_hash_at_its_own_seq(self):
        ...

    def test_a_journal_shorter_than_the_snapshot_is_a_problem(self):
        ...

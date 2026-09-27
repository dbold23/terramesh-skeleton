"""python3 -m unittest discover -s station/vault"""
from __future__ import annotations
import hashlib
import json
import os
import stat
import sys
import tempfile
import unittest
import zipfile
import terramesh_vault as tv

def sha(data: bytes) -> str:
    ...

def ledger(files: dict[str, bytes]) -> bytes:
    ...

def make_export(folder: str, name: str, carried: dict[str, bytes], offloaded: dict[str, bytes] | None=None, captured: dict[str, bytes] | None=None, tamper: str | None=None) -> str:
    ...

class VaultTests(unittest.TestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_ingest_stores_each_file_once_and_is_idempotent(self):
        ...

    def test_blobs_are_read_only_and_named_by_hash(self):
        ...

    def test_receipt_lists_only_media_with_copies(self):
        ...

    def test_delta_export_after_offload_keeps_the_originals(self):
        ...

    def test_delta_naming_media_the_vault_lacks_is_refused(self):
        ...

    def test_tampered_entry_is_refused_and_nothing_recorded(self):
        ...

    def test_media_that_differs_from_the_capture_ledger_is_refused(self):
        ...

    def test_unsafe_paths_are_refused(self):
        ...

    def test_scrub_repairs_from_a_mirror(self):
        ...

    def test_cli_ingest_remove_source_and_receipt(self):
        ...

    def test_cli_skips_files_that_are_not_surveys(self):
        ...

    def test_a_copied_survey_folder_keeps_what_arrived_intact(self):
        ...

    def test_receipt_golden_fixture_matches_swift(self):
        """station/vault/fixtures/receipt.json is decoded by TerraMeshCore's StationReceiptTests."""
        ...

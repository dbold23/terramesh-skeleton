"""The hash-chained audit journal: tamper detection and concurrent appends."""
import json
import os
import shutil
import tempfile
import threading
import unittest
from tests.support import PHOTOGRAMMETRY
from twinlib import audit

def some_event(index):
    ...

class TestChain(unittest.TestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def lines(self):
        ...

    def rewrite(self, lines):
        ...

    def test_an_empty_journal_verifies(self):
        ...

    def test_appends_chain_and_verify(self):
        ...

    def test_hash_is_the_canonical_sha256(self):
        ...

    def test_a_flipped_byte_is_caught(self):
        ...

    def test_a_reorder_is_caught(self):
        ...

    def test_a_dropped_event_is_caught(self):
        ...

    def test_two_threads_produce_a_dense_sequence(self):
        ...

    def test_authors_are_listed_once_each(self):
        ...

    def test_an_unknown_action_is_refused(self):
        ...

    def test_builder_author_uses_the_environment_override(self):
        ...

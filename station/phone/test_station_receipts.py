import hashlib
import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
import station_receipts

class ReceiptTests(unittest.TestCase):

    def test_only_files_matching_the_ledger_are_listed(self):
        ...

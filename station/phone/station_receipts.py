"""Write Station receipts for survey folders copied off the phone, and optionally push them back.

The phone frees a survey's photos, video, depth, 3D and sound only against a receipt that lists
each file with the SHA-256 the phone's own capture ledger recorded (SurveyStore+Storage.swift).
This script hashes the Station's copy of every file the ledger names and puts in the receipt
only those that match, so a file that arrived damaged or not at all stays on the phone.

    uv run python station/phone/station_receipts.py "<Station>/inputs/field-test-2026-09-25"
    uv run python station/phone/station_receipts.py "<Station>/inputs/..." --push --device <udid>

Survey folders are the app's Documents/Surveys/<uuid>/ copied as they are (ledger.jsonl inside).
Receipts are written to <folder>/../station-receipts/<uuid>.json. With --push each receipt is
copied into the app's Documents/Surveys/StationReceipts/ with `xcrun devicectl`. Nothing on the
phone is deleted by this script: the person taps Free up in Phone storage.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

def sha256(path: Path) -> str:
    ...

def ledger_entries(survey: Path) -> dict[str, dict]:
    """Latest ledger line per path. The phone verifies the chain itself before it trusts a receipt."""
    ...

def receipt_for(survey: Path, station: str) -> tuple[dict, int, int]:
    ...

def main() -> int:
    ...

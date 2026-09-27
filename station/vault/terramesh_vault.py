"""TerraMesh Station vault: one verified, deduplicated copy of every survey file the phone sends.

    python3 station/vault/terramesh_vault.py --root "<Station>" ingest <export.zip | survey folder> [...] [--remove-source]
    python3 station/vault/terramesh_vault.py --root "<Station>" receipts [--survey ID ...] [--push --device UDID]
    python3 station/vault/terramesh_vault.py --root "<Station>" scrub
    python3 station/vault/terramesh_vault.py --root "<Station>" materialize <surveyID> --out <folder>
    python3 station/vault/terramesh_vault.py --root "<Station>" mirror <folder>
    python3 station/vault/terramesh_vault.py --root "<Station>" stats

Standard library only, so it runs with any python3 (or `uv run --no-project`).

Layout under <Station>/vault (see docs/storage.md):

    station.json                          this vault's id and name, made on first use
    blobs/ab/<sha256>                     each distinct file once, named by its SHA-256, read-only
    surveys/<SURVEY-ID>/versions/*.json   one record per imported export: every path with its hash
    surveys/<SURVEY-ID>/current.json      the newest hash of every path any export carried
    mirrors.json                          other folders holding a copy of the blobs (a second drive)

Why it saves space: a survey exported again after review re-sends every photo, and the phone may
send only what changed once its originals have gone (an export that lists them under
`offloaded` in provenance.json). Both land as the handful of files that actually differ.

A blob is written to a temporary file, hashed as it is written, flushed to disk and only then
renamed into place, so a crash or an unplugged drive never leaves a blob whose name is not its
hash. Nothing in the vault is ever deleted by this tool.

`receipts` writes one Station receipt per survey (the StationReceipt the app reads from
Documents/Surveys/StationReceipts/, same format as station/phone/station_receipts.py) listing the
media files the vault holds, byte for byte, and how many verified copies of each exist. The phone
frees a file only when the receipt's hash equals the one its capture ledger recorded and the file
on the phone still hashes to it (TerraMeshCore SurveyStore+Storage.swift), so a stale or foreign
receipt can never cost it an original. With --push the receipts go to the phone over USB.

`ingest` takes export ZIPs (AirDrop, ~/Downloads) and survey folders copied straight out of the
app's container (Documents/Surveys/<uuid>/). A ZIP is all-or-nothing; a copied folder keeps
whatever arrived intact and leaves out (and reports) any media file that no longer matches the
capture ledger, which then stays on the phone.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
import zipfile
RECEIPT_SCHEMA_VERSION = 1

class VaultError(Exception):
    ...

def now_iso() -> str:
    ...

def sha256_file(path: str) -> str:
    ...

def check_relative_path(name: str) -> str:
    """Mirrors StationKit Snapshot.checkRelativePath: relative, normalised, no traversal."""
    ...

def is_offloadable(path: str) -> bool:
    ...

def write_json(path: str, value) -> None:
    """Atomic: temporary file, fsync, rename."""
    ...

def ledger_latest(data: bytes, survey_id: str) -> dict[str, dict]:
    """The last ledger line for each path, when the chain holds; {} when it does not."""
    ...

class Vault:

    def __init__(self, station_root: str):
        ...

    def blob_path(self, sha: str, root: str | None=None) -> str:
        ...

    def has_blob(self, sha: str, size: int | None=None) -> bool:
        ...

    def put_stream(self, source, expected_sha: str | None, expected_size: int | None) -> tuple[str, int, bool]:
        """Stores a stream as a blob. Returns (sha256, size, newly_stored). A stream whose hash or
        size is not what the export declared is refused and nothing is stored."""
        ...

    def ingest(self, archive_path: str) -> dict:
        """Stores every entry of one survey export and records the version. Idempotent."""
        ...

    def ingest_folder(self, folder: str) -> dict:
        """Stores a survey folder copied from the phone. Media that no longer match the capture
        ledger are left out and reported, so a damaged copy never earns a receipt."""
        ...

    def _record_version(self, survey_id: str, version: dict, source_sha: str, stamp: str) -> bool:
        ...

    def versions(self, survey_id: str) -> list[dict]:
        ...

    def rebuild_current(self, survey_id: str) -> dict:
        """The newest hash of every path any export carried or listed as offloaded. Paths never
        drop out: a later export that no longer carries a file does not erase the vault's copy."""
        ...

    def current(self, survey_id: str) -> dict:
        ...

    def survey_ids(self) -> list[str]:
        ...

    def mirrors(self) -> list[str]:
        ...

    def mirror(self, destination: str) -> dict:
        """Copies every blob the destination lacks, verifying each copy by hash, and remembers
        the destination so receipts can count it."""
        ...

    def copies(self, sha: str, size: int) -> int:
        ...

    def receipt(self, survey_id: str, deep: bool=False) -> dict:
        """The Station receipt for one survey (TerraMeshCore StationReceipt): every offloadable
        file the vault holds, with how many verified copies exist. `deep` re-hashes each blob
        before listing it."""
        ...

    def iter_blobs(self):
        ...

    def scrub(self) -> dict:
        """Re-hashes every blob. A damaged blob is reported (and restored from a mirror that holds a
        good copy); it is never silently deleted."""
        ...

    def materialize(self, survey_id: str, out: str) -> int:
        """Rebuilds a survey's folder from blobs, as hard links where the filesystem allows (no
        extra space) and copies otherwise. Blobs are read-only, so workers cannot alter them."""
        ...

    def stats(self) -> dict:
        ...

def main(argv: list[str] | None=None) -> int:
    ...

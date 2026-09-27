"""Wildbook bulk-import sheets (https://wildbook.docs.wildme.org/data/bulk-import-beta.html).

One row per encounter, in the Wildbook standard column names, with the confirmed stills copied
beside the sheet under names Wildbook accepts (letters, digits, dots and spaces only). The
individual ID column is filled only from a person's review, never from the matcher.
"""
from __future__ import annotations
import csv
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .snapshot import VIEWS, Encounter

def local_time(moment: datetime | None, zone: str) -> datetime | None:
    ...

def encounter_time(encounter: Encounter) -> datetime | None:
    ...

def media_name(encounter: Encounter, view: str, index: int) -> str:
    ...

def comments(encounter: Encounter, proposal: str | None) -> str:
    ...

def mark_text(mark: dict) -> str:
    ...

def sex_and_stage(encounter: Encounter) -> tuple[str, str]:
    """Wildbook's sex and life stage, from what the operator recorded. Life stage only for a male
    whose claspers were checked by touch."""
    ...

def row_for(encounter: Encounter, media: list[tuple[str, str]], *, zone: str, individual: str='', submitter: str='', proposal: str | None=None) -> dict:
    ...

def write_sheet(folder: Path, rows: list[dict]) -> list[Path]:
    ...

def export(encounter: Encounter, folder: Path, *, zone: str, individual: str='', submitter: str='', proposal: str | None=None) -> dict:
    """Copies the confirmed stills and writes the one-encounter sheet. Returns the row."""
    ...

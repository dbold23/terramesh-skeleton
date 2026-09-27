"""Synthetic phone exports with records marked as individuals, for tests.

The patterned animals come from shark-match's tests (tests/synthetic.py): each individual has its
own spot pattern per view, photographed with a different pose, scale, light and background each
time. Here the pattern stands in for a turtle's head scutes or a fluke's markings.
"""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
import uuid
from pathlib import Path
from PIL import Image

def photograph(individual: str, view: str, seed: int):
    ...

def catalogue_photos(folder: Path, individuals: list[str], encounters: int, view: str, tags: dict[str, str] | None=None, mirror_of: str | None=None) -> Path:
    """Photos plus the register CSV `catalog import` reads (image,individual,view,encounter,tag).

    With `mirror_of`, each photo is that view's pattern flipped left to right: a turtle whose two
    sides of the head are mirror images, as Adam et al. (2025) found."""
    ...

def write_register(path: Path, rows: list[dict]) -> Path:
    ...

def make_export(folder: Path, records: list[dict], *, seed: int) -> Path:
    """An unpacked export with one observation per record.

    A record is {"group", "individual" (whose pattern is photographed), "views": [...], optional
    "tag", "tagSource", "confidential", "individualField": False to leave the mark off}.
    """
    ...

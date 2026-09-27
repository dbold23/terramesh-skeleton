"""Builds a TMGC occurrence cube from a GBIF occurrence download.

    uv run --project station/workers/bioclip-rerank bioclip-geo-cube \\
        --occurrences 0012345-260923123456789.zip --doi 10.15468/dl.abcdef \\
        --region California \\
        --out "$HOME/Library/Application Support/TerraMesh Station/inputs/gbif-cube/california.tmgc"

Input is a GBIF occurrence download, "Simple" or Darwin Core Archive (both tab-separated, one
occurrence per line), either the ZIP GBIF sends or the file inside it; there's no need to unzip it. The file is streamed once, so a whole-state download of tens of
millions of rows works in constant memory apart from the cube itself.

Two vocabularies:

- Without `--vocabulary`, every species in the download becomes a taxon. This is the regional cube
  the Mac worker ranks against.
- With `--vocabulary BioCLIPTaxonomy.json`, the taxa are the phone's embedding bank, in bank order,
  so `SpeciesEmbeddingBank.softmaxScores(query:priors:)` can take the scores directly. A bank name
  GBIF files under another species (records often carry the observer's older name) takes that
  species' records. Bank names the download never mentions at all are listed as unmatched and, by
  default, score like any species not recorded nearby: in a regional download they are almost
  always species from elsewhere, and scoring them higher would favour out-of-range look-alikes.
  Raise `--unmatched-presence` only for a download that covers the bank's whole range.

Nothing here touches the network: download the file from gbif.org yourself, and keep its DOI,
which GBIF's data licences require you to cite.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import math
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from . import geocube
from .kit import sha256_file, utc_now

def open_rows(path: Path):
    """Yields dicts from a GBIF Simple or Darwin Core Archive download (ZIP, or the file inside it)."""
    ...

def load_vocabulary(path: Path) -> list[dict]:
    """Leaves of a RecognitionTaxon JSON (export-bioclip.py), in leaf_class_id order."""
    ...

def is_dwca(path: Path) -> bool:
    """A Darwin Core Archive download carries occurrence.txt; a Simple one a single CSV."""
    ...

def canonical(name: str | None) -> str:
    ...

def binomial(name: str | None) -> str:
    """'Pisaster ochraceus (Brandt, 1835)' -> 'pisaster ochraceus'; '' for anything that isn't one."""
    ...

def build(rows, *, cell_degrees: float, constants: geocube.ScoringConstants, vocabulary: list[dict] | None, max_uncertainty_m: float, min_records: int, progress=None):
    """Returns (taxa, cells, unmatched taxon indices, stats). Pure: `rows` is any iterable of GBIF simple-download dicts."""
    ...

def _int(value):
    ...

def main(argv=None) -> int:
    ...

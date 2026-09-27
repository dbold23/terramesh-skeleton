"""Fetches model files into Station's model cache once, checking each against a pinned size and SHA-256
when one is known. A file is only ever moved into place whole, so an interrupted download never
leaves a half-written model behind."""
from __future__ import annotations
import hashlib
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Remote:
    url: str
    name: str
    size: int | None = None
    sha256: str | None = None

def fetch(remote: Remote, folder: Path) -> Path:
    """Returns the cached file, downloading it first if it is missing or does not match its pins.
    Raises ConnectionError when the download fails or arrives damaged (the job can be retried)."""
    ...

def _matches(path: Path, remote: Remote) -> bool:
    ...

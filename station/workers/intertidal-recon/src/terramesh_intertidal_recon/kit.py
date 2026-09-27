"""Helpers for the Station worker contract (station/WORKERS.md). Standard library only.

Copy this file into a new worker unchanged. It is vendored rather than shared so that a worker's
version and uv.lock fully describe what it runs.
"""
from __future__ import annotations
import datetime as _dt
import hashlib
import json
import mimetypes
import os
import random
import signal
import sys
from pathlib import Path
EXIT_OK = 0
EXIT_BAD_INPUT = 2
EXIT_UNSUPPORTED = 3
EXIT_TEMPORARY = 75

class WorkerError(Exception):
    """Raise with an exit code from section 7. The message becomes the last line of stderr."""

    def __init__(self, message: str, code: int=EXIT_BAD_INPUT) -> None:
        ...

class Job:
    """Everything one run needs: the snapshot, the output directory, params and Station's environment."""

    def __init__(self, snapshot: Path, out: Path, params: dict) -> None:
        ...

    def has(self, relative: str) -> bool:
        ...

    def path(self, relative: str) -> Path:
        ...

    def manifest(self) -> dict:
        ...

    def jsonl(self, relative: str):
        """Yields each JSON object in a journal. A missing journal yields nothing."""
        ...

    def input(self, name: str) -> Path | None:
        """The folder of a declared input, or None when an optional one is absent. Read-only."""
        ...

    def files(self, prefix: str='') -> list[dict]:
        ...

    def progress(self, fraction: float, stage: str, detail: str | None=None) -> None:
        ...

    def warn(self, message: str) -> None:
        ...

    def log(self, message: str) -> None:
        ...

    def record_model(self, *, name: str, version: str, weights: Path, licence: str, commercial_use: bool, source: str) -> None:
        ...

    def write_json(self, relative: str, value) -> Path:
        ...

    def finish(self, *, kind: str, title: str, summary: dict, claim_level: str='descriptive', roles: dict[str, str] | None=None, worker_name: str, worker_version: str) -> dict:
        """Lists every file in `out` as an artefact and writes layer.json last. `roles` maps an
        artefact path to phone, full or debug; unlisted files default to full."""
        ...

def sha256_file(path: Path) -> str:
    ...

def utc_now() -> str:
    ...

def milliseconds_to_iso(value) -> str | None:
    """The app encodes dates as milliseconds since 1970."""
    ...

def main(argv, *, name: str, version: str, run, describe_extra: dict | None=None) -> int:
    """Implements `terramesh-worker describe` and `terramesh-worker run`. `run(job)` does the work
    and ends by calling job.finish(...)."""
    ...

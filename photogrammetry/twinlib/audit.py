"""Append-only, hash-chained audit journal.

One JSON object per line.  ``hash`` is the SHA-256 of the canonical JSON of
every field but ``hash`` itself; ``prev_hash`` is the previous line's ``hash``,
and 64 zeros at ``seq`` 0.  Appends take an advisory lock on the file and open
it ``O_APPEND``, so two writers on the same machine cannot interleave a partial
line or duplicate a sequence number.
"""
from __future__ import annotations
import fcntl
import getpass
import hashlib
import json
import os
import socket
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

def now_iso() -> str:
    """UTC timestamp with milliseconds, the spelling used throughout the package."""
    ...

def canonical_bytes(event: dict) -> bytes:
    """Canonical bytes for hashing: every field but ``hash``, sorted, compact."""
    ...

def event_hash(event: dict) -> str:
    ...

def builder_author() -> dict:
    """The author record every builder-written event carries."""
    ...

def new_event(author: dict, action: str, target: dict, payload: dict | None=None) -> dict:
    """An event without chain fields; :func:`append_event` fills those in."""
    ...

def _last_line(handle) -> bytes:
    """Read the final non-empty line of an open binary file without loading it all."""
    ...

def head(path) -> tuple:
    """``(seq, hash)`` of the last event, or ``(-1, ZERO_HASH)`` for a new journal."""
    ...

def append_event(path, event: dict) -> dict:
    """Append ``event``, assigning ``seq``, ``prev_hash`` and ``hash`` under a lock.

    Returns the stored event.  The file is opened ``O_APPEND`` so the write is
    atomic for line-sized payloads, ``flock``ed so the sequence number read and
    the write are one critical section, and fsynced before the lock is dropped.
    """
    ...

def append_events(path, events) -> list:
    """Append several events in order; each is chained to the one before."""
    ...

@dataclass
class ChainReport:
    ok: bool
    length: int
    head_hash: str
    first_bad_seq: int | None = None
    reason: str | None = None

    def __bool__(self) -> bool:
        ...

def verify_chain(path) -> ChainReport:
    """Re-walk the journal, reporting the first sequence number that fails."""
    ...

def iter_events(path):
    """Stream the journal one event at a time."""
    ...

def authors(path) -> list:
    """Distinct authors in first-seen order, for the collaborators strip."""
    ...

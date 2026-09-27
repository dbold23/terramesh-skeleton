"""Hand-written validators for the twin package (no jsonschema).

``validate_package`` returns a list of human-readable problems and an empty list
when the package is valid.  Every rule in ``SCHEMA.md`` that can be checked from
the files alone is checked here, including the ones that keep the package
honest: a registered transform must carry a matrix and an RMSE, an unregistered
one must carry no matrix and a reason, an anchor may only hold a site position
when it is registered, and a tag may never claim identity.
"""
from __future__ import annotations
import json
import logging
import os
from . import audit

def _is_number(value) -> bool:
    ...

def _require(problems, condition, message):
    ...

def _matrix_ok(value) -> bool:
    ...

def _vector3_ok(value) -> bool:
    ...

def _read_json(path):
    ...

def _iter_jsonl(path):
    ...

def validate_record(kind: str, record) -> list:
    """Validate one journal record.  ``kind`` in anchor|tag|control_point|event."""
    ...

def validate_transform(record, known_layers=None) -> list:
    ...

def validate_layer(layer, root, layer_path) -> list:
    ...

def _check_integrity_snapshot(audit_path, integrity, report, notes) -> list:
    """``twin.json.integrity`` is what the chain looked like when the builder wrote it,
    not a live invariant.

    The viewer appends to ``audit.jsonl`` through the local server and never rewrites
    the manifest, so the moment anybody tags anything the recorded count and head fall
    behind.  That is correct behaviour for an append-only journal, so it is a note.

    What stays a problem: a journal *shorter* than the recorded count, or a recorded
    head hash that is not the hash at the recorded position — either means the journal
    was rewritten rather than appended to.
    """
    ...

def _event_at_seq(audit_path, seq):
    """The event at one seq, without holding the journal in memory."""
    ...

def validate_package(root, notes: 'list | None'=None) -> list:
    """Validate a whole twin package.  Returns ``[]`` when it is valid.

    ``notes`` is an optional list that receives non-fatal observations.  The only one
    today is append-only growth of ``audit.jsonl`` past the manifest's snapshot; pass a
    list to read them, or leave it out and they are logged at INFO on the
    ``twinlib.schema`` logger.  Notes are never problems and never affect the return
    value.
    """
    ...

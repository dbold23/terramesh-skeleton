"""Shared helpers so every test file runs under pytest and under unittest."""
import os
import sys

def lfs_file_present(path):
    """True when `path` holds its real bytes. A checkout without `git lfs pull` leaves a
    small text pointer in its place, which is no more usable than a missing file."""
    ...

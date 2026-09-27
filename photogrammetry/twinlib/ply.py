"""Minimal PLY reader/writer.

Only what the twin builder needs: ``ascii`` and ``binary_little_endian`` headers
for a single ``vertex`` element, streaming reads through ``numpy.fromfile`` with
a structured dtype, and a binary little-endian writer.  A 1 M x 59 float splat
file is never held in memory in full.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
import numpy as np

class PlyError(ValueError):
    """Malformed or unsupported PLY file."""

@dataclass
class PlyHeader:
    path: str
    fmt: str
    vertex_count: int
    properties: list
    data_offset: int
    little_endian: bool

    @property
    def dtype(self) -> np.dtype:
        ...

    @property
    def itemsize(self) -> int:
        ...

    def names(self) -> list:
        ...

def read_header(path) -> PlyHeader:
    """Parse the header of ``path``.  Only the ``vertex`` element is described."""
    ...

def iter_vertices(path, chunk: int=200000, header: PlyHeader | None=None):
    """Yield the vertex element as structured numpy arrays of at most ``chunk`` rows.

    The whole file is never read into memory; binary data comes through
    ``numpy.fromfile`` with an explicit ``count``.
    """
    ...

def read_all(path, header: PlyHeader | None=None) -> np.ndarray:
    """Read every vertex into one structured array.  Only for small files."""
    ...

def header_bytes(array: np.ndarray, comments=()) -> bytes:
    ...

def write_binary(path, array: np.ndarray, comments=()) -> str:
    """Write a structured array as a binary little-endian PLY, atomically."""
    ...

class BinaryWriter:
    """Streaming binary PLY writer for arrays produced in chunks.

    The vertex count is not known until the last chunk, so the header is written
    with a placeholder and patched in place before the file is moved into place.
    """

    def __init__(self, path, dtype: np.dtype, comments=()):
        ...

    def write(self, block: np.ndarray) -> None:
        ...

    def close(self) -> str:
        ...

    def __enter__(self):
        ...

    def __exit__(self, *exc):
        ...

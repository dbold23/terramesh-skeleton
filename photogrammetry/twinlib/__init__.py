"""TerraMesh twin package library.

Readers and writers for the twin package format described in ``SCHEMA.md``
(beside this file).  Nothing here promotes a number above the claim level it
arrived with, and nothing here writes into a survey export or a run directory.

Modules
-------
ply         minimal PLY header parser and streaming reader/writer (no plyfile)
similarity  Umeyama similarity fit and a RANSAC gate (no scipy)
earth       WGS84 east/north tangent plane, port of GeographicAlignment
audit       append-only hash-chained event journal
schema      hand-written validators for every file in the package
colmap      COLMAP model reader (pycolmap) in the ARKit camera convention
arkit       streaming readers for the phone survey export
"""
__all__ = ['ply', 'similarity', 'earth', 'audit', 'schema', 'colmap', 'arkit']
SCHEMA_VERSION = 1

"""Build a TerraMesh twin package from survey exports and photogrammetry runs.

The builder reads its sources read-only — an export ZIP is read through
``zipfile`` and never extracted into the source tree, a run directory is never
written to — hashes everything it uses, writes one layer per thing the viewer can
draw, registers every layer frame to the site frame, appends the audit events
that record what it did, and writes ``twin.json`` last through a temporary file
and ``os.replace`` so a reader never sees a half-built manifest.

What the package claims
-----------------------
Positions live in each layer's own frame; ``transforms.json`` says how (and
whether) that frame reaches the site frame.  Splats, meshes and coverage patches
are derived views, not measured surfaces.  A frame with no accepted fit is
written ``unregistered`` with a reason rather than placed approximately.

Idempotence
-----------
The build key is the SHA-256 of the sorted source hashes, the builder version and
the options that change the output.  A second run with the same key does nothing
unless ``--force`` is given.  Journals (``audit.jsonl``, ``anchors.jsonl``,
``tags.jsonl``, ``control-points.jsonl``) are appended to and never rewritten.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import numpy as np
import register_twin
from twinlib import arkit, audit, colmap as colmap_reader, ply, schema
SCHEMA_VERSION = 1
DEFAULT_SPLAT_BUDGET = 300000
DEFAULT_THUMB_SIZE = 256
EVIDENCE_MAX_PX = 1024
EVIDENCE_QUALITY = 80
THUMB_QUALITY = 70
OPACITY_FLOOR = 0.02
LARGEST_SCALE_DROP = 0.005
SPLAT_CELL = 0.5
SPLAT_CELL_SHARE = 0.02

def sha256_file(path, block: int=1 << 20) -> str:
    ...

def sha256_bytes(data: bytes) -> str:
    ...

def write_json(path, payload) -> str:
    """Write JSON through a temporary file, then rename it into place."""
    ...

def read_json(path):
    ...

def copy_image(source, destination, max_px: int, quality: int) -> str:
    """Downscale (never upscale) and re-encode one JPEG into the package."""
    ...

def directory_bytes(path) -> int:
    ...

class LayerWriter:
    """Collects the manifest rows and layer.json files for one package."""

    def __init__(self, root):
        ...

    def path_for(self, layer_id) -> str:
        ...

    def add(self, layer_id, *, visit_id, kind, producer, counts, source_sha256, frame_id=None, version=1, caveats=None, original_path=None, extra=None):
        ...

def write_sparse_ply(path, xyz, rgb) -> int:
    """A sparse cloud as binary little-endian PLY: float x y z, uchar r g b."""
    ...

def copy_sparse_ply(source_path, destination) -> int:
    """Re-encode any x/y/z(+rgb) PLY as the package's binary sparse form, streamed."""
    ...

def stations_payload(frame_id, stations) -> dict:
    ...

def _sigmoid(x):
    ...

def build_splat_lod(source_path, destination, budget: int, seed: int=0, chunk: int=200000) -> dict:
    """Stream a 3DGS PLY down to ``budget`` splats and write a standard 3DGS PLY.

    Three things happen, in this order, and each is recorded:

    1. every ``f_rest_*`` band is dropped (view-dependent colour the viewer does
       not evaluate), leaving the DC term;
    2. splats with ``sigmoid(opacity) < 0.02`` are dropped as invisible, and the
       largest 0.5 % by ``mean(exp(scale))`` are dropped as blobs that swamp a
       frame without describing a surface;
    3. the rest are importance-sampled by ``opacity * mean scale`` with a spatial
       cap of 2 % of the budget per 0.5-unit cell, so one dense corner cannot
       spend the whole budget.

    The file is read twice and never held in memory in full.
    """
    ...

def copy_mesh(obj_path, mtl_path, texture_path, destination_dir) -> dict:
    """Copy the RealityKit mesh verbatim, with the two file references rewritten.

    The geometry and the texture bytes are untouched; only ``mtllib`` in the OBJ
    and ``map_Kd`` in the MTL are rewritten, because the files are renamed to the
    fixed names the viewer looks for.
    """
    ...

class VisitSpec:

    def __init__(self, identifier, date=None, export=None, run=None):
        ...

    @property
    def kind(self) -> str:
        ...

def _pair_visits(exports, runs, ids, dates) -> list:
    ...

class Builder:

    def __init__(self, *, site, twin_root, site_name=None, exports=(), runs=(), visit_ids=(), visit_dates=(), splat_budget=DEFAULT_SPLAT_BUDGET, thumb_size=DEFAULT_THUMB_SIZE, force=False, dry_run=False, report=(), seed=0, site_frame='auto', pinned_layer=None, quiet=False, encounters=(), reconstruct_binary=RECONSTRUCT_BINARY, encounter_detail='reduced', reconstruct=True):
        ...

    def say(self, text):
        ...

    def build_encounter_mesh(self, visit, source, prefix, arc_stills, hashes) -> list:
        """Run Object Capture over the encounter's arc stills and add one half-mesh layer.

        The stills are what the operator walked around the animal collecting: high-resolution
        frames with ARKit pose and intrinsics, every five degrees of subject-centred azimuth in
        three height bands. RealityKit is given the images only; its coordinate scale is its own
        and is not metric, which is why the layer is a `derived_view` and carries the caveat.

        A half-mesh of one side of a handled animal is a visit layer. Two encounters of what may
        be one animal are compared as temporal tracks under an operator tag, never as an asserted
        identity, and nothing in this function establishes that two meshes are the same animal.
        """
        ...

    def options_key(self) -> dict:
        ...

    def build_key(self, source_hashes) -> str:
        ...

    def collect_sources(self) -> list:
        """Hash every file the build will read.  Runs hash only the files used."""
        ...

    def _run_files(self, run) -> list:
        ...

    def plan(self) -> list:
        """A deterministic description of what a build would write."""
        ...

    def _planned_layers(self, visit) -> list:
        ...

    def build(self) -> str:
        ...

    def _build_visit(self, visit):
        ...

    def _rk_frame_id(self, visit, prefix) -> str:
        """Which layer stands for RealityKit's estimated local frame in this visit.

        Every RealityKit product (mesh, sparse cloud, poses) is in one frame, so one
        layer represents it and the others share its frame_id. Without an export the
        stations layer built from poses.json is that representative; with an export
        the stations layer belongs to ARKit instead, so the mesh takes the role.
        """
        ...

    def _build_run_layers(self, visit, prefix, hashes, frames) -> list:
        ...

    def _splat_frame_id(self, run, prefix) -> str:
        """Which frame the splat was trained in, read from the training config."""
        ...

    def _build_export_layers(self, visit, prefix, hashes, source, manifest, frames) -> list:
        ...

    def _register(self, visit_rows):
        ...

    def _register_visit(self, visit, pinned):
        ...

    def _register_realitykit_frame(self, visit, spec, frame_id, inputs):
        """Place RealityKit's estimated local frame (mesh, sparse cloud, poses).

        With a phone export in hand the RealityKit poses are fitted to the ARKit
        trajectory by the same exact-name join, then composed with whatever places
        the ARKit frame in the site frame. Without one there is nothing to fit
        against, and the frame is left unregistered rather than guessed at.
        """
        ...

    def _write_manifest(self, visit_rows, key, report):
        ...

def _visit_of(layer_id):
    ...

def _pycolmap_version() -> str:
    ...

def _hypot(*values):
    ...

def write_tag_reports(root) -> list:
    """Write ``cache/tag-<id>.json`` for every tag, with deltas only where earned.

    A delta is printed only between rows of the same measurement ``kind`` **and**
    ``method_version``.  It is significant when ``|delta| > 2 * hypot(uncertainty
    a, uncertainty b, registration a, registration b)``.  When any one of those
    four is missing the verdict is ``null`` with an ``unsupported_reason``: an
    unknown uncertainty is not a small one.
    """
    ...

def _delta(row_a, row_b, a, b) -> dict:
    ...

def build_parser() -> argparse.ArgumentParser:
    ...

def encounter_visit_ids(encounters, exports, visit_ids) -> list:
    """Resolve each ``--encounter`` to the visit id it names.

    An encounter may be given as a path that is also in ``--export`` (the usual case), as a path
    that is not (it is appended to the exports), or as a bare visit id. Resolving it here rather
    than in the builder keeps one rule: a visit is an encounter because it was named as one, never
    because a heuristic guessed from its contents.
    """
    ...

def main(argv=None) -> int:
    ...

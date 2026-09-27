"""Register every layer frame in a twin package to the site frame.

What a transform here claims
----------------------------
A similarity fitted to two sets of camera centres says how well those two pose
sets agree, in the units of the target frame.  It is not accuracy against ground
truth, and it does not make a reconstruction metric on its own: the only metric
scale a COLMAP piece can inherit is the one carried by an ARKit trajectory
(``scale_source: "arkit_similarity"``).  A fit against RealityKit's estimated
local frame inherits RealityKit's own unverified scale
(``scale_source: "realitykit_similarity"``, units ``unscaled``).

The joins are exact, never fuzzy.  Export images are written as
``images/<frameID>.jpg`` (``SurveyStore.swift:175``), so a COLMAP or RealityKit
image name is the frame id plus ``.jpg`` and joins ``frames.jsonl`` by string
equality.  Frames whose ``trackingState`` is not "normal" are dropped before the
fit, because ARKit's own pose is the reference and a limited pose is not one.

Gates
-----
* at least ``MIN_MATCHES`` (8) shared names after the tracking filter,
* RANSAC inlier threshold ``max(0.05, 0.02 * reference path length over the
  matched span)``,
* at least ``MIN_MATCHES`` inliers and at least half the matches kept, because
  the reported RMSE is an inlier RMSE and three lucky inliers out of thirty are
  not a registration,
* accept when ``rmse_pct_of_reference_path <= 3``; otherwise the transform is
  written ``unregistered`` with an ``unsupported_reason`` and no matrix.
"""
from __future__ import annotations
import argparse
import json
import os
import socket
import sys
import uuid
import numpy as np
from twinlib import arkit, colmap as colmap_reader, earth, similarity
MIN_MATCHES = 8
ACCEPT_RMSE_PCT = 3.0
MIN_INLIER_FRACTION = 0.5
MIN_THRESHOLD_M = 0.05
THRESHOLD_PATH_FRACTION = 0.02
RANSAC_ITERATIONS = 500

def _computed_by() -> dict:
    ...

def transform_record(from_frame, *, state, method, matrix=None, scale=None, matched=0, inliers=0, rejected=0, rmse=None, median_err=None, max_err=None, rmse_pct=None, uncertainty=None, scale_source='none', units='unscaled', vertical_state='unresolved', inputs=None, unsupported_reason=None, caveats=None, computed_at=None, transform_id=None) -> dict:
    """One ``transforms.json`` record, with every field the schema names present."""
    ...

def _now() -> str:
    ...

def identity_pin(layer_id, units='unscaled', caveats=None) -> dict:
    """The one transform that pins a ``local_unscaled`` site to a layer."""
    ...

def shared_names(source_centres: dict, reference_centres: dict) -> list:
    """Image names present in both pose sets, in sorted order.  An exact string join."""
    ...

def arkit_reference_centres(frames, *, require_normal=True) -> dict:
    """``{image name: centre}`` from ARKit frames, dropping non-normal tracking."""
    ...

def fit_to_reference(from_frame, source_centres, reference_centres, *, scale_source, units, reference_label, inputs=None, min_matches=MIN_MATCHES, accept_rmse_pct=ACCEPT_RMSE_PCT, seed=0, with_scale=True, caveats=None, dropped_note=None) -> dict:
    """Fit ``source_centres`` onto ``reference_centres`` and report it as a transform.

    ``reference_centres`` are already in the target (site) frame.  The reference
    path length is measured over the matched span only, so the percentage is the
    residual against the part of the trajectory the fit actually saw.
    """
    ...

def _straightness(points):
    ...

def register_colmap_to_arkit(layer_id, model, frames, *, inputs=None, seed=0, segment_id=None) -> dict:
    """A COLMAP piece against the ARKit trajectory: the only metric scale it can get."""
    ...

def register_realitykit_to_arkit(layer_id, poses, frames, *, inputs=None, seed=0) -> dict:
    """RealityKit's estimated local frame against ARKit; the same exact-name join."""
    ...

def register_colmap_to_realitykit(layer_id, model, poses, *, inputs=None, seed=0) -> dict:
    """A COLMAP piece against RealityKit poses, when there is no phone export.

    This is the precedent set by ``runs/curb-02/learned-sfm/baseline.py``: fit a
    similarity to the camera centres of the frames the two share.  RealityKit's
    frame is the only one that spans the whole walk, but its scale is its own
    estimate and nothing has verified it, so the result is ``unscaled`` and the
    scale source is ``realitykit_similarity``.
    """
    ...

def segment_to_site(layer_id, placement, site_anchor, *, inputs=None, caveats=None, state='prior', method='earth_placement') -> dict:
    """Place one segment's local frame into the site's ENU frame.

    ``earth-placement.json`` gives a matrix into ENU at *that segment's own*
    reference coordinate; :func:`twinlib.earth.rebase_segment` shifts it onto the
    site anchor.  The vertical offset between the two references is not observed
    by anything in the export, so ``vertical_state`` stays ``unresolved``.
    """
    ...

def _hypot(*values):
    ...

def enu_prior(layer_id, matrix_column_major, *, placement_a, placement_b, inputs=None, caveats=None) -> dict:
    """A visit placed beside another purely because both carry an ENU placement.

    Nothing was matched between the two visits; the agreement is only as good as
    the two GPS placements, so the state is ``prior``, never ``registered``.
    """
    ...

def control_point_pairs(path, anchors_by_id, visit_a, visit_b):
    """Read ``control-points.jsonl`` and return the (a, b) position pairs it declares."""
    ...

def fit_control_points(layer_id, pairs, labels=None, *, both_metric, inputs=None, caveats=None, seed=0) -> dict:
    """Fit a transform from declared control-point pairs.

    Rigid when both visits are already metric (a scale would only absorb error);
    a similarity otherwise.  The worst point is named, because a control-point
    fit is only as stable as the points the operator declared.
    """
    ...

def fit_icp(*args, **kwargs):
    """Not implemented.

    The plan's ICP step refines a visit-to-visit fit on the sparse clouds inside
    an operator-declared stable mask, and rejects the result when it moves the fit
    by more than the control-point RMSE without lowering the residual.  None of
    that exists yet, and a fake ICP would print a number nothing earned, so this
    raises instead.
    """
    ...

def _describe(record) -> str:
    ...

def main(argv=None) -> int:
    ...

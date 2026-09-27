"""Compare learned-SfM camera poses against the three COLMAP pieces and against
the RealityKit trajectory (the only reference that spans all 163 frames).

Alignment is a similarity (Umeyama, with scale) fitted to camera CENTRES.
Caveat recorded per piece: the curb walk is close to a straight line, so the
roll about the walk axis is weakly observed by a centre-only fit. Rotation
agreement is therefore reported alignment-free, as the error in the relative
rotation between consecutive frames.
"""
import json, sys, os
import numpy as np

def umeyama(src, dst):
    ...

def ang(R):
    ...

def fit_report(Cmod, Cref):
    ...

def rk_centres():
    ...

def main(model_dir, label):
    ...

"""Run MapAnything (Apache checkpoint) on the curb-02 keyframes.

Modes:
  image-only : load_images() on the folder, no calibration supplied
  calibrated : preprocess_inputs() with COLMAP pinhole intrinsics per view

Outputs: poses.json, points.ply, metrics.json
"""
import os
import argparse, json, time, glob
import numpy as np
import torch

def write_ply(path, xyz, rgb):
    ...

def main():
    ...

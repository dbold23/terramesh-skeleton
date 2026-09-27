"""Baseline: how well do the COLMAP pieces themselves agree with RealityKit?
Gives a reference scale for the learned-model numbers."""
import json, os, numpy as np
import sys
from compare import umeyama, rk_centres

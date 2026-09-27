"""Export a TerraMesh twin package as a Darwin Core Archive.

    .tools/photogrammetry/bin/python photogrammetry/export_dwc.py         --package twin/curb --out twin/curb-dwca         --dataset-name "Curb walk, 2026" --rights-holder "CSUMB"         --creator "Sambold, D." --license CC-BY-4.0 --validate

Writes `event.txt`, `occurrence.txt`, `extendedmeasurementorfact.txt`,
`multimedia.txt`, `meta.xml` and `eml.xml` into the output folder, and the same
six files zipped as `<site-id>-dwca.zip` beside that folder.  `--validate`
reads the written archive back and checks it structurally.  The mapping, and
what it deliberately leaves blank, is documented in `photogrammetry/DWC.md`.
"""
from __future__ import annotations
import argparse
import os
import sys
from twinlib import dwc

def build_parser():
    ...

def main(argv=None):
    ...

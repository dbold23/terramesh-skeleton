"""Match evidence from the walk round the animal: the same capture that builds the twin.

The walk's posed stills are unrolled into body maps (shark-morphometrics' bodymap.py): each
side of the shark in its own coordinates, snout to caudal origin, back to belly, with the
handlers masked out. A body map replaces a hand-confirmed view photograph: it is square to
every part of the flank at once, the same size whatever the standoff, and the same spot lands on
the same pixel in every encounter. The landmarks a person picked for the measurements (the
shark-landmarks input) fix which end is the head. Without them the one flank the walk saw is
offered both as a left and as a right flank, each marked as an assumption; neither is ever
added to the catalogue.
"""
from __future__ import annotations
from pathlib import Path
from terramesh_shark_morphometrics import bodymap
from terramesh_shark_morphometrics.cameras import SnapshotError as StillsError, load_stills
from terramesh_shark_morphometrics.cli import DEFAULTS as MEASURE_DEFAULTS, find_landmarks, fit_landmarks, read_picks
from .snapshot import Encounter, ViewImage

def add_walk_round(encounter: Encounter, snapshot: Path, views: list[str], landmarks_folder: Path | None, folder: Path, min_coverage: float) -> int:
    """Adds a body map per view the walk saw to `encounter.images`. Returns how many."""
    ...

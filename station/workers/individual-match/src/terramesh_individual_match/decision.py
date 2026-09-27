"""The open-set decision for one sighting: appearance scores (shark-match's WildFusion decision)
combined with the tag number, when one was read.

Neither names an individual. A tag match says "the number on this tag is recorded for T"; the
photos say "this looks most like T". When the two disagree, a person decides.
"""
from __future__ import annotations
from .catalog import Catalog
from .groups import GROUPS, MIRRORED
from .tags import compare, skeleton

def tag_evidence(tag: str | None, catalog: Catalog | None) -> dict | None:
    """What the catalogue says about a tag read in the field."""
    ...

def weigh_mirrored(decision: str, reasons: list[str], ranked: list[dict], accept: float | None) -> tuple[str, list[str]]:
    """Keeps a flipped comparison from deciding on its own. Calibrations are fitted on same-side pairs,
    so a score from a turtle's left side against a right side, flipped, is a lead for a person, not a
    resighting; and heads compared only that way cannot show a turtle is new."""
    ...

def combine(group: str, decision: str, reasons: list[str], ranked: list[dict], tag: dict | None, catalog: Catalog | None) -> tuple[str, list[str]]:
    """Adds the tag's evidence to the appearance decision. `decision` and `reasons` come from
    shark-match's `decide`, or are no_comparison / insufficient_evidence when nothing was scored."""
    ...

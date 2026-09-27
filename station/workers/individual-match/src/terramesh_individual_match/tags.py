"""Tag numbers: how they are compared, and which near misses a person should look at.

A tag read from a photograph can be off by a character: text recognition confuses O and 0, I and
1, S and 5, B and 8, and a weathered tag loses a digit. So an exact match is reported as a match,
and a number one confusable character or one edit away is reported as a near miss for a person to
check. Neither names an individual: tags fall off and get replaced, and two programmes can use
the same series.
"""
from __future__ import annotations
MAXIMUM_LENGTH = 32

def normalise(text: str | None) -> str:
    """Upper-cased, with everything but letters, digits and hyphens removed."""
    ...

def skeleton(tag: str) -> str:
    """The tag with hyphens dropped and confusable characters folded."""
    ...

def edit_distance(a: str, b: str, limit: int=2) -> int:
    """Levenshtein distance, giving up (returning `limit`) once it is certain to reach `limit`."""
    ...

def compare(read: str, known: str) -> str | None:
    """"exact", "near" or None for a tag read in the field against a catalogued one."""
    ...

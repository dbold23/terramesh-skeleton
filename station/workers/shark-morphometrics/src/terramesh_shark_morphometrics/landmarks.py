"""The landmarks a person picks and the measurements made between them.

Measurements are straight point-to-point distances between two landmarks, the "direct"
measurements of Compagno's shark morphometrics (FAO Species Catalogue vol. 4, 1984), not
distances over the curve of the body. Proportions are given as a percentage of precaudal length,
because PCL does not depend on how the tail is lying, and total length does.

Sevengills (Hexanchiformes) have one dorsal fin; leopard sharks have two. Neither species has a
precaudal pit or a forked tail, so there is no fork length: PCL runs to where the upper caudal
lobe begins.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Landmark:
    id: str
    label: str
    hint: str

@dataclass(frozen=True)
class Measurement:
    id: str
    code: str
    label: str
    start: str
    end: str

def landmarks_for(mission: str) -> list[Landmark]:
    ...

def measurements_for(mission: str) -> list[Measurement]:
    ...

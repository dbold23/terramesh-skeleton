"""TerraMesh experience readout: what each survey's guides saw against what got saved.

    python3 station/experience/experience_readout.py <survey folder | folder of surveys> [...] [--html]

Reads `experience.jsonl`, the dev-only log a Debug or TestFlight build writes into each survey
folder (ios/EXPERIENCE-LOG.md). Point it at one survey folder, at a vault `materialize` output,
or at a phone copy such as inputs/phone-2026-09-26e; it finds every log below the path.

For each survey it prints one block: how long it ran, frames per second the capture accepted,
each guide's sightings against its saves, heat and battery, errors, and a list of flags such as
"cube seen 212 times, saved 0". With --html it also writes `experience.html` beside each log: a
timeline of the guides' states, heat and the main counters, readable without anything else.

Standard library only. Run on request; nothing here runs on its own, and nothing is uploaded.
The log holds no positions or clock times, and this readout adds none.
"""
from __future__ import annotations
import argparse
import html
import json
import os
import sys
from dataclasses import dataclass, field
SLOW_SAVE_MS = 1000

@dataclass
class Survey:
    path: str
    twinstant: str | None = None
    bad_lines: int = 0

    @property
    def duration(self) -> float:
        ...

    @property
    def ended(self) -> str | None:
        ...

    def totals(self) -> dict[str, int]:
        ...

    def states(self, name: str) -> list[tuple[float, str, dict]]:
        ...

    def system(self) -> list[dict]:
        ...

    def errors(self) -> list[dict]:
        ...

def load(path: str) -> Survey:
    ...

def find_logs(paths: list[str]) -> list[str]:
    ...

def total(totals: dict[str, int], keys: list[str]) -> int:
    ...

def first_time(survey: Survey, predicate) -> float | None:
    ...

def longest_ms(survey: Survey, key: str) -> float | None:
    ...

def timing_summary(survey: Survey, key: str) -> str | None:
    """'n 412, slower than 1 s: 3, longest 2600 ms', from the bucket counters and window maxima."""
    ...

def tap_summary(survey: Survey) -> str | None:
    """'subject box hit 4, gone 1; camera missBox 3, noBoxes 7', from the tap lines."""
    ...

def five_to_name(survey: Survey) -> dict | None:
    """Five to name at Finish: cards answered, skipped, and seconds, split by the phone's organism
    reading (2 living, 1 no reading, 0 not living). None when the survey logged no answers."""
    ...

def flags(survey: Survey) -> list[str]:
    """Plain sentences for what went wrong or looks wrong. Empty when nothing stands out."""
    ...

def clock(seconds: float) -> str:
    ...

def battery_span(survey: Survey) -> tuple[float | None, float | None]:
    ...

def summary(survey: Survey) -> str:
    ...

def _segments(states: list[tuple[float, str, dict]], end: float) -> list[tuple[float, float, str]]:
    ...

def render_html(survey: Survey) -> str:
    ...

def main(argv: list[str] | None=None) -> int:
    ...

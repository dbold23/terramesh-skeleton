"""The kinds of individual this worker re-finds, and which photographs of each it compares.

Keep in step with `IndividualGroup` and `IndividualView` in TerraMeshCore/IndividualSighting.swift:
the raw values here are what the phone writes into `observation.individual`.

- Sea turtles are told apart by the scutes on the sides of the head, which do not change with
  age. The two sides of one turtle's head look alike as mirror images (Adam et al. 2025), so a
  left side is compared with left sides as it is, and with right sides flipped left to right.
  Many nesting turtles also carry a numbered flipper tag.
- Whales are told apart by the underside of the tail fluke: its black and white pattern, scars
  and the shape of the trailing edge. A humpback lifts it on a deep dive.
- A tagged plant is identified by its numbered tag. The photographs of the plant only confirm the
  tag was read right and show how the plant has changed; plants change too much between visits
  for appearance alone to name one.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Group:
    title: str
    views: tuple[str, ...]
    matched_views: tuple[str, ...]
    tags: bool
    tag_is_identity: bool
    mirrored: tuple[tuple[str, str], ...] = ()

    def opposite(self, view: str) -> str | None:
        ...

def group(name: str) -> Group:
    ...

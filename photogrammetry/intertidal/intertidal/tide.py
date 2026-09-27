"""Tide heights on the model: the cube frame's vertical tied to a NOAA tidal datum.

A run's heights are already true millimetres along gravity (the cube sets the scale, ARKit
the up direction). What they lack is one number: how high the model sits against the tide
station's datum (MLLW). Two ways to get it:

- **Waterline marks.** In the app the operator aims the screen's centre at the line where
  calm water meets the rock and taps "Water's edge". Each mark is a LiDAR point's height in
  ARKit's world at a known time. NOAA's measured water level at that minute is its height
  above MLLW, so every point of the model gets one too. Accuracy is set by how far the
  station's water differs from the site's (distance, swell, wind) and by how steady the
  waterline was, not by the model: about ±0.1-0.15 m on a calm day near a station, and
  0.2-0.4 m in swell.
- **A dry scan (lower limit only).** With no marks, the scan still shows rock that was out
  of the water when it was photographed. So its lowest scanned point was at least as high as
  the water then, and every height here is a lower limit ("at least").

From the height of each point this module gives the station's datum lines (MLLW, MLW, MSL,
MHW, MHHW, and HAT when the station publishes it) and how many hours a day each point is
under still water, from a year of the station's hourly tide predictions. Waves wet rock
above still water, so hours underwater is a lower limit on hours wet.

Station records come from the NOAA CO-OPS API (US public domain) and are cached in the
run's `tide/` folder, so a run fetches them once and later runs work offline.
"""
from __future__ import annotations
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np
STATION_TO_SITE_M = 0.1
DRIFT_PER_METRE = 0.01

def _utc(ms: float) -> datetime:
    ...

def _read_jsonl(path: Path) -> list[dict]:
    ...

@dataclass
class SurveyTide:
    """The survey's own tide reading, as the phone joined it."""
    station_id: str | None
    station_name: str | None
    level_m: float | None = None
    sigma_m: float | None = None
    time: datetime | None = None

def survey_tide(folder: Path) -> SurveyTide | None:
    """From tide.json (builds that export it) or the tideWaterLevel measurement."""
    ...

def station_named(text: str) -> str | None:
    """The app's station whose name, or its name without the state, appears in `text`."""
    ...

def station_name(station_id: str) -> str | None:
    ...

@dataclass
class Mark:
    """One tap on the water's edge, or on a band's upper edge: its height in ARKit's world
    (metres, up) and when."""
    time: datetime
    arkit_y_m: float
    camera_m: np.ndarray | None
    segment: str | None
    point_m: np.ndarray | None = None
    band: str | None = None

def _marks(folder: Path, kind: str) -> list[Mark]:
    ...

def waterline_marks(folder: Path) -> list[Mark]:
    ...

def zonation_marks(folder: Path) -> list[Mark]:
    """Band edge taps: the upper limits of bands of life, and the wet line, as the operator named them."""
    ...

def frame_segments(folder: Path, names: list[str]) -> set[str]:
    """The ARKit tracking segments the run's frames came from. A mark placed in another segment
    lives in a different ARKit world and cannot be carried into the model."""
    ...

class Station:
    """A CO-OPS station's records, fetched once and cached in `cache`."""

    def __init__(self, station_id: str, cache: Path, fetch: bool=True):
        ...

    def _get(self, url: str, name: str) -> dict:
        ...

    def _series(self, product: str, begin: datetime, end: datetime, interval: str | None, name: str) -> dict:
        ...

    def datums(self) -> dict[str, float]:
        """The station's datums in metres above its MLLW."""
        ...

    def levels(self, begin: datetime, end: datetime) -> tuple[np.ndarray, np.ndarray, str]:
        """Water level above MLLW round a survey: measured (6-minute) where the station
        measures, else its predictions. Times as seconds since 1970."""
        ...

    def year(self, ending: datetime) -> np.ndarray:
        """Hourly predicted water level above MLLW for the 365 days before `ending`."""
        ...

def _rows(rows) -> tuple[np.ndarray, np.ndarray]:
    ...

def hilo_to_hourly(times: np.ndarray, values: np.ndarray, at: np.ndarray) -> np.ndarray:
    """The rule of twelfths as a curve: between each high and low, a half cosine."""
    ...

def level_at(times: np.ndarray, values: np.ndarray, when: datetime) -> float:
    ...

def hours_under(heights_m: np.ndarray, year: np.ndarray) -> np.ndarray:
    """Mean hours a day under still water for each height, from hourly levels."""
    ...

@dataclass
class Anchor:
    """height above MLLW (m) = offset_m + (point . up) / 1000, for a point in cube mm."""
    method: str
    offset_m: float
    uncertainty_m: float | None
    lower_limit: bool

def from_marks(marks: list[Mark], fit, up: np.ndarray, times: np.ndarray, levels: np.ndarray, model_centre_mm: np.ndarray, level_source: str) -> Anchor:
    """Each mark's height in cube mm follows from the ARKit-to-cube fit: along `up` (the fit's
    image of ARKit's +Y) a point's height is scale * Y + t . up."""
    ...

def from_dry_scan(heights_mm: np.ndarray, water_m: float, water_source: str) -> Anchor:
    """No marks: the scan's lowest rock was out of the water when photographed."""
    ...

def colours(hours: np.ndarray, band_hours: float | None=2.0) -> np.ndarray:
    """Colour by hours under water, in bands of `band_hours` so equal bands read as contours."""
    ...

def render(path: Path, xyz: np.ndarray, rgb: np.ndarray, up: np.ndarray, anchor: Anchor, datums: dict[str, float], survey_level: float | None, face_normal: np.ndarray | None, outline: np.ndarray | None, title: str, width: int=1400, height: int=1000) -> None:
    """A side view of the scan shaded by hours underwater, with the datum lines across it."""
    ...

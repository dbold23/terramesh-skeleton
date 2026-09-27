"""Heat on the shore: when a low tide leaves a band of life out in hot sun.

Mussels, barnacles and surfgrass die in numbers when a midday low tide meets a hot, still, sunny
day (the June 2021 heat dome cooked mussel beds from Washington to British Columbia). A band's
upper edge is its most exposed part. With the site's own tide (waterline.SiteTide) we know when
that edge is out of the water; with a weather forecast we know how hot the air is and how strong
the sun. Out of the water a dark shell in full sun runs well above the air, so:

    shell temperature ~ air + SUN_GAIN_C * sun (kW/m2)      while emersed
    shell temperature ~ sea temperature                      while under water

This leaves out wind, the shell's heat lag and damp rock, so it is a warning, not a measurement.
The thresholds are rough values from the literature for each band, not measured here. Waves
wet a band up to its lift above still water (reef.json waterline.waves_lift_bands_mm), so a band
counts as out of the water only when still water plus that lift is below its edge.
"""
from __future__ import annotations
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
SUN_GAIN_C = 12.0
SEA_C = 13.0
DEFAULT_LIMITS_C = (32.0, 38.0)

@dataclass
class BandDay:
    band: str
    day: str
    hours_out_in_daylight: float
    hottest_c: float | None
    hottest_at: str | None
    hours_over_stress: float
    level: str

    def to_json(self) -> dict:
        ...

def read_forecast(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A weather CSV with columns time (ISO, UTC unless it says otherwise), air_c, sun_wm2."""
    ...

def shell_temperature(air_c: np.ndarray, sun_wm2: np.ndarray, out: np.ndarray, sea_c: float=SEA_C) -> np.ndarray:
    ...

def forecast(site, station_times: np.ndarray, station_levels: np.ndarray, times: np.ndarray, air_c: np.ndarray, sun_wm2: np.ndarray, edges_mm: dict[str, float], lift_mm: float=0.0, sea_c: float=SEA_C, zone: str='America/Los_Angeles', step_min: float=10.0) -> list[BandDay]:
    """Each band's days over the forecast: hours out of the water in daylight, its hottest shell
    temperature and when, and hours over its stress limit."""
    ...

def summary(days: list[BandDay]) -> list[str]:
    """One line per band-day that is not ok, worst first."""
    ...

"""Waterlines: a place's own tide from its waterline taps, and its habitats predicted from that tide.

Three steps, each usable alone.

1. The site's tide. `fit_site_tide` extends the reef's subordinate-station fit (reef.fit_local_tide:
   site = intercept + ratio * station(t - lag)) with the two things that set a slough or a lagoon
   apart from open rock:
     - the flood and the ebb run late by different amounts (the channel fills fast and drains slowly,
       or the other way round), and
     - low tides stop at a floor: the channel drains to its sill or bed and no lower.
   Each extra term is kept only when the taps pay for it (BIC), so an open reef stays a plain lag
   and ratio. The result is a virtual tide gauge: `site_water` turns any stretch of the station's
   record, such as a year of predictions, into the site's own water.

2. Hydroperiod. For every height: the share of time under water, the longest dry spell of a typical
   day, and how often it floods. Plants and animals answer to these, not to height: two sites with
   different tides put the same band at different heights but under the same hydroperiod.

3. Habitat. A band's upper edge, tapped on the phone ("Band edge"), becomes a hydroperiod. That
   hydroperiod then predicts where the band sits on any other scan with a fitted tide, on this site
   under a higher sea, and (with no taps yet) where slough habitats usually sit, from starting
   guesses tied to the station's datums. Waves lift bands above still water; a site's wet line above
   still water (reef.json) is taken off before a band becomes a hydroperiod and put back after.

Everything here is heights in one site frame (mm) and water levels in that frame; nothing is located.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
LAG_MIN, LAG_MAX = (-60.0, 240.0)
MIN_TAPS = 8
FLOOR_TOL_MM = 15.0
MIN_AT_FLOOR = 2
RATIO_RANGE = (0.2, 1.6)
SEA_LEVEL_RISE_M = (0.25, 0.5, 1.0)

@dataclass
class SiteTide:
    """site water (mm, site frame) = max(floor_mm, intercept_mm + 1000 * ratio * station(t - lag)),
    with lag = flood_lag_min while the site's water rises and ebb_lag_min while it falls."""
    usable: bool
    reason: str | None
    model: str | None = None
    taps: int = 0
    ratio: float | None = None
    intercept_mm: float | None = None
    flood_lag_min: float | None = None
    ebb_lag_min: float | None = None
    floor_mm: float | None = None
    rms_mm: float | None = None
    dropped: int = 0

    def water(self, times: np.ndarray, station_times: np.ndarray, station_levels: np.ndarray, sea_rise_m: float=0.0) -> np.ndarray:
        """The site's water (mm) at `times` from the station's record, optionally with the sea higher."""
        ...

    def meaning(self) -> str:
        ...

    def to_json(self) -> dict:
        ...

def _station_at(t: np.ndarray, times: np.ndarray, levels: np.ndarray, flood_lag: float, ebb_lag: float) -> np.ndarray:
    """The station's level at t less the flood or the ebb lag. Flood or ebb is judged by whether the
    station was rising half-way between the two lags earlier."""
    ...

def _linear(x: np.ndarray, z: np.ndarray):
    ...

def _fit_floor(x: np.ndarray, z: np.ndarray):
    """The best floor for these taps: (rss, ratio, intercept, floor) or None. From a few starting
    floors near the lowest taps: fit the line to the taps well above the floor, then take as on
    the floor the taps the line would put below it, and repeat."""
    ...

def lag_window(t: np.ndarray, times: np.ndarray) -> tuple[float, float]:
    """The lags (min) the station's record can test for these taps, within LAG_MIN..LAG_MAX."""
    ...

def _search(t, z, times, levels, two_lags: bool, floor: bool, near: tuple[float, float] | None=None):
    """The best fit of one model over the lag grid: (rss, ratio, intercept, flood, ebb, floor).
    `near` skips the coarse grid and searches round a known answer (for the jackknife)."""
    ...
OUTLIER_SIGMAS = 4.0
OUTLIER_MIN_MM = 50.0

def fit_site_tide(marks: list[tuple[float, float]], times: np.ndarray, levels: np.ndarray, jackknife: bool=True) -> SiteTide:
    """Fit the site's tide to its waterline taps: (unix seconds, water mm in the site frame) against
    the station's record (unix seconds, m above its MLLW). Tries a plain lag, flood and ebb lags, a
    low-tide floor, and both, and keeps the one the taps support best (BIC). Taps far off the first
    fit (more than 4 robust sigmas and 5 cm) are left out once and the fit is made again: the
    phone's own watch can catch a wave or a patch of shade."""
    ...

def _fit_site_tide(marks: list[tuple[float, float]], times: np.ndarray, levels: np.ndarray, jackknife: bool=True) -> SiteTide:
    ...

def from_json(data: dict) -> SiteTide:
    """A SiteTide back from reef.json's waterline.site_tide."""
    ...

def from_reef(local) -> SiteTide:
    """The reef's plain lag-and-ratio fit (reef.LocalTide) as a SiteTide."""
    ...

def from_tie(offset_m: float) -> SiteTide:
    """No fitted tide: the station's water moved by the waterline tie (height above MLLW =
    offset_m + z / 1000), so site water z = 1000 * (station - offset_m)."""
    ...

@dataclass
class Hydroperiod:
    """For a ladder of heights (mm): share of the time under water, the longest dry spell of a
    typical day (median over days, hours), and floods a day."""
    z_mm: np.ndarray
    under: np.ndarray
    longest_dry_h: np.ndarray
    floods_per_day: np.ndarray
    highest_mm: float
    lowest_mm: float

    def under_at(self, z_mm) -> np.ndarray:
        ...

    def dry_at(self, z_mm) -> np.ndarray:
        ...

    def z_for_under(self, under: float) -> float:
        """The height at which the share of time under water is `under` (the lowest such height)."""
        ...

def hydroperiod(water_mm: np.ndarray, step_h: float=1.0, z_mm: np.ndarray | None=None) -> Hydroperiod:
    """Hydroperiod from a regular series of the site's water (mm), e.g. a year hourly."""
    ...

@dataclass
class Habitat:
    name: str
    label: str
    under: float
    source: str
    z_mm: float | None = None
    above_highest_mm: float | None = None
    below_lowest_mm: float | None = None

    def to_json(self) -> dict:
        ...

def habitat_at(name: str, label: str, z_mm: float, hydro: Hydroperiod, source: str, tapped_z: float | None=None) -> Habitat:
    """A habitat whose upper edge is at z_mm on the site that `hydro` describes."""
    ...

def habitats_from_taps(levels: dict[str, dict], hydro: Hydroperiod, labels: dict[str, str], splash_mm: float=0.0) -> list[Habitat]:
    """Band upper edges tapped on the phone (reef.band_levels) as hydroperiods. The wet line is
    not a habitat and is skipped. `splash_mm`, the site's wet line above still water, is taken
    off first: waves, not the tide, hold a band that far up."""
    ...

def slough_priors(station_hydro: Hydroperiod, datums: dict[str, float]) -> list[Habitat]:
    """The slough starting guesses as hydroperiods, measured on the station's own year (so they
    carry to a site through its tide, not its height). `station_hydro` is in mm above MLLW."""
    ...

def merge(tapped: list[Habitat], guesses: list[Habitat]) -> list[Habitat]:
    """Taps replace guesses of the same name; highest (least under water) first."""
    ...

def place(habitats: list[Habitat], hydro: Hydroperiod, splash_mm: float=0.0) -> list[tuple[Habitat, float]]:
    """Each habitat's upper edge as a height on this site (mm), waves added back."""
    ...

def classify(z_mm: np.ndarray, edges: list[tuple[Habitat, float]]) -> np.ndarray:
    """Index of the habitat each height falls in (a habitat runs from its upper edge down to the
    next one's); -1 above the highest, NaN heights stay -2."""
    ...

def areas(classes: np.ndarray, habitats: list[Habitat], cell_m2: float) -> dict[str, float]:
    ...

@dataclass
class Prediction:
    habitats: list[Habitat]
    edges_mm: dict[str, dict[str, float]]
    areas_m2: dict[str, dict[str, float]]
    classes: dict[str, np.ndarray]
    squeezed: dict[str, list[str]]
    hydro_now: Hydroperiod

    def to_json(self) -> dict:
        ...

def predict(site: SiteTide, year_times: np.ndarray, year_levels: np.ndarray, cell_z_mm: np.ndarray, cell_m2: float, tapped_levels: dict[str, dict] | None=None, labels: dict[str, str] | None=None, datums: dict[str, float] | None=None, setting: str='rocky', splash_mm: float=0.0, rises: tuple[float, ...]=SEA_LEVEL_RISE_M) -> Prediction | None:
    """Habitat on every cell of a scan now and with the sea higher, from the site's tide over a
    year of the station's record, the bands tapped here, and (for a slough) the starting guesses."""
    ...

def render(path, classes_now: np.ndarray, classes_later: np.ndarray, habitats: list[Habitat], later_label: str, title: str, palette: dict[str, tuple] | None=None, px_per_cell: int=4) -> None:
    """Two plan maps side by side: habitat now and with the sea higher, with a legend."""
    ...

"""A synthetic slough: a mixed-semidiurnal station, a site up a channel whose flood and ebb run late by
different amounts and whose low tides stop at the channel floor, taps across a low tide, and a plan
of the bank from channel to upland."""
import numpy as np
T0 = 1790000000.0
CONSTITUENTS = ((12.42, 0.5, 0.0), (12.0, 0.13, 1.1), (12.66, 0.11, 2.3), (23.93, 0.37, 0.7), (25.82, 0.23, 2.9))
MSL = 0.95

def station(t):
    ...

def year():
    ...

def datums_of(levels):
    """MLLW-based datums from an hourly series, roughly as NOAA derives them."""
    ...

def site(t, truth=TRUTH):
    ...

def _record():
    ...

def record():
    """The station's measured water round the survey, every 6 minutes."""
    ...

def low_tide_taps(every_min=15.0, span_h=8.0, noise_mm=12.0, seed=0, truth=TRUTH):
    """Taps across the lowest low water of the survey's first days: falling, on the floor, rising."""
    ...

def bank(cell_mm=250.0, width_m=40.0, depth_m=12.0, seed=0):
    """Plan heights (mm, site frame) of a bank rising from the channel (west) to upland (east): a
    channel, a gently sloping flat, a marsh plain with a scarp, then a steeper upland edge."""
    ...

"""The scale bar as one more rigid tag set: it shares the scale with the cubes and sets it."""
import unittest
import numpy as np
from intertidal.cube import CUBE_FOLDER, SCALE_BAR_GROUP, SCALE_BAR_SPEC, Cube, spec_paths
from intertidal.scale import fit

def rotation(axis, degrees):
    ...

class ScaleBarTests(unittest.TestCase):

    def located(self, placements: dict[int, tuple], misprint: dict[int, float] | None=None, noise_mm: float=0.15, seed: int=0):
        """(keys, sfm) for every corner of the given sets, placed in a world (mm) and seen in the gauge."""
        ...

    def test_the_bar_loads_as_one_more_rigid_set(self):
        ...

    def test_the_bar_sets_the_scale_and_a_misprinted_cube_is_left_out(self):
        ...

    def test_the_bar_alone_is_its_own_frame(self):
        ...

    def test_a_field_cube_tag_with_a_cube_id_is_named_and_dropped(self):
        ...

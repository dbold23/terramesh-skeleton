# Marker artwork

`tags-a4-actual-size.svg` is an A4 sheet of six 80 × 80 mm adhesive graphics.
Print at **100% / actual size**, disable fit-to-page, and measure each black
square after printing. Its nominal side is **64 mm**; the white label side is
80 mm. PNG copies carry 254 dpi metadata, but SVG physical dimensions are less
likely to be ignored by layout software. Verify scale regardless of format.

`tag-N-tile-84mm.svg/png` shows the 84 mm white printed tile with a 10 mm clear
white margin around its black square. Do not put lettering, screws, cord, or
bumper geometry inside the clear marker artwork. The OpenSCAD cell data is in
`../source/markers.scad`; module `field_cube_marker_black(id, z_base, height)`
places canonical artwork top toward the tile's +Y direction.

The printed option has 0.4 mm raised black graphics on a 1.2 mm white base.
Raised edges can cast shadows; physically test detection and corner stability
under the lighting and camera angles you intend to use. Adhesive artwork on a
flat blank tile is an alternative, but its surface offset differs from the
raised print. Update the configuration to match the actual mounted surface.
For manifold printable geometry, the SCAD module dilates the black cell union
internally by a 0.02 mm radius before extruding and clips it to the original
64 mm square. This resolves diagonal cell contacts without enlarging the
external detected square. Ideal SVG and PNG adhesive artwork is unchanged.

`nominal-target.json` defines OpenCV canonical TL,TR,BR,BL corners in mm. It is
nominal CAD geometry, not measured calibration. Measure finished faces and
verify with an independent distance in the reconstructed scene before making
accuracy claims. Recheck seating and dimensions after impacts or replacement.

**Orientation:** each official AprilRobotics source PNG is rotated **180 degrees**
when producing the artwork and SCAD cell arrays, matching OpenCV's canonical
`DICT_APRILTAG_36h11` bitmap. This matters for corner order even though an ID
decodes under any quarter-turn rotation. All generated artwork tops map to face
`+v` in the JSON. Do not substitute raw upstream PNGs without rotating them or
changing the face transforms. When OpenCV is available, generation verifies
exact bitmap equality and canonical corners under four rotations and a
perspective warp for every marker.

Official source: https://github.com/AprilRobotics/apriltag-imgs/tree/master/tag36h11
Family definition: https://github.com/AprilRobotics/apriltag/blob/master/tag36h11.c
OpenCV convention: https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
AprilTag scale convention: https://github.com/AprilRobotics/apriltag#pose-estimation

The cached official PNGs and family definition are in `upstream/`. The image
and family sources use the BSD 2-Clause license; retain the accompanying
`LICENSE-apriltag-imgs.txt` notice when distributing the derived marker assets.
`verification.json` records source hashes, exact cell counts, equality between
the PNG bitmaps and the independent family code/bit-coordinate definition,
unique marker count, and verification of the nominal corner edge lengths.

Regenerate with `python3 ../source/generate_markers.py` (NumPy and Pillow).
After the initial asset download, regeneration uses the cached sources offline.

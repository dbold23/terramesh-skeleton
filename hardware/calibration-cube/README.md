# Intertidal calibration cube

A 40 mm cube with an AprilTag (`tag36h11`) on all six faces: ids 0–4 on the top and
sides, and id 500 on the bottom. Or, with `--bottom socket`, five tags and a 1/4 in dowel
socket in the bottom for a pole, or with `--bottom anchor`, five tags and a ballast pocket
and cord loop for surge. Set it at the mouth of a crevice before filming. It gives the
[intertidal photogrammetry](../../photogrammetry/intertidal/README.md) video a known
metric scale, a fixed origin, and a live closeness and sharpness check.

| File | What it is |
| --- | --- |
| [calibration_cube.scad](calibration_cube.scad) | OpenSCAD model, parts `body`, `ink`, `preview` |
| [tag_bits.scad](tag_bits.scad) | generated tag bit patterns and face frames |
| [cube-spec.json](cube-spec.json) | generated metric corner coordinates, read by the scale solver and the app |
| [stickers.svg](stickers.svg) | generated 1:1 sticker sheet with a 50 mm check bar |
| [generate.py](generate.py) | writes the three generated files; the one source of truth for tag geometry |
| [tiled_cube.scad](tiled_cube.scad), [make_tiled_3mf.py](make_tiled_3mf.py) | the tiled version: a white core and five flat-printed tag tiles, and its Bambu plate |
| [make_3mf.py](make_3mf.py) | writes `calibration-cube.3mf`: one object, white body and black ink parts on their own filaments (Bambu Studio / Orca, or `--format prusa`) |

## Why a cube

A flat scale bar or a single marker has to face the camera. At a crevice, the camera
moves around and into the opening, so a flat target is edge-on for much of the pass.
A cube always shows at least one face, and usually two or three, from any angle above
the rock. Two or more faces also put corners on different planes, which constrains
the scale much better than four coplanar points. A cube's scale only comes from its own
40 mm, though, so for anything much longer than a crevice (a shark, a reef strip's scale, a rock
face) add the [scale bar](../scale-bar/README.md), whose 882 mm baseline is about ten times
more precise. The solver reports how much the scale
moves when any one face is left out, which catches a misread or glared tag.

## Printing

- **Material:** PETG or ASA. PLA softens in the sun and creeps in salt water. Use
  matte filament if you can, because gloss glints like wet rock.
- **Two colours (best):** run `python3 make_3mf.py` and open `calibration-cube.3mf` in
  Bambu Studio or Orca. It loads as one object with white on filament 3 and black on
  filament 4 (change with `--body-filament` / `--ink-filament`), and carries 0.2 mm layers,
  0.15 mm elephant foot compensation, no supports and no brim. Add `--bottom socket` for
  the pole version and `--format prusa` for PrusaSlicer. It prints bottom face down, so the
  bottom tag is laid on the plate, the flattest face the printer makes. Or export the two parts as
  STLs and load both as one multi-material object. The black cells are inlaid 0.8 mm deep and flush with the
  surface, so they survive being wedged against rock.
  ```sh
  openscad -D 'part="body"' -o cube-body.stl calibration_cube.scad   # add -D 'bottom="socket"' for the pole
  openscad -D 'part="ink"'  -o cube-ink.stl  calibration_cube.scad
  ```
- **One colour:** print `body` in white and fill the pockets with a black paint pen or
  tinted epoxy. Or print a plain cube and apply `stickers.svg` printed on waterproof
  vinyl. Check that the 50 mm bar on the sheet measures 50.0 mm first.
- 0.2 mm layers, 4 walls, **100% infill** for any cube that goes in water. At 40% infill the
  sealed air inside makes a 40 mm cube lighter than the seawater it displaces (about 45 g
  against 66 g), so it floats off. At 100% it sinks, but only by about 15 g; for surge, print the
  anchor version below.

## Anchor version (surge)

`bottom = "anchor"` (or `python3 make_3mf.py --bottom anchor`) keeps the five tags and puts a
sealed ballast pocket and a cord loop in the bottom. Nothing about the tags changes, so the
phone, `cube-spec.json` and the pipeline treat it like the socket version.

- **Ballast:** a 26 mm pocket with a cone roof, filled at a print pause. In Bambu Studio, right
  click the layer slider at **23.0 mm** and add a pause; when the printer stops, pour in steel
  shot (4.5 mm steel BBs or stainless balls, about 36 g) level with the pocket's straight wall,
  and resume. The cone roof then closes over it. The shot is sealed in, so plain steel is fine.
- **Weight:** with 100% infill the body is about 64 g; with the shot, about 100 g, which sinks
  with about 35 g to spare. Never print the anchor version without the shot: the empty pocket
  leaves it neutral, and it drifts off.
- **Cord loop:** two holes in the bottom joined by a tunnel. Thread 2-3 mm cord through and tie
  it off to your wrist, a dive weight or a rock wrap. It leaves no mark on the reef.
- The bottom has the 5 mm ticks, like the socket version.

## Tiled version (sharper tags)

Printed in one piece with the socket down, the four side tags are built up the wall a layer
at a time, so every tag edge is a stack of layer lines and the side faces can come out
slightly out of square. [tiled_cube.scad](tiled_cube.scad) prints each tag as a flat 2 mm
tile face down on the plate instead, where the edges are as sharp as the printer gets and
the face is as flat as the plate. A white core holds the tiles in pockets:

- Two pins on the back of each tile fit only its own pocket, and only one way round. The
  Mac needs to know which tag is on which face and which way up, and the tests check that no
  tile fits another pocket or its own turned.
- Each pocket is 0.1 mm deeper than its tile. Glue with a few dots of CA gel, then set the
  cube that face down on glass or a flat tile until it cures. The tile's face and the
  pocket's rim both rest on the glass, so the tag ends up flush with the cube face and the
  glue layer doesn't matter.
- The tags land exactly where the one-piece cube puts them, so `cube-spec.json`, the phone's
  tag codes and the pipeline need no change.
- The bottom stays plain, with the dowel socket, and prints on the plate. A tag there would
  sit on rock or on the pole.

```sh
python3 make_tiled_3mf.py --body-filament 3 --ink-filament 4   # calibration-cube-tiled.3mf
```

The plate holds the core (socket down) and the five tiles (face down, three to a row). It
fits a 180 mm bed. Use a textured PEI plate for a matte face that doesn't glint. After
assembly, measure the tag edge as below, and also measure across each pair of opposite tagged
faces (left to right, front to back, top to bottom). Give the mean of those three readings as
`--measured-edge-mm` (Station: `measured_edge_mm`). The fit uses the distance between faces as well
as the tag sizes, so a cube that came out 0.3 mm large would otherwise read about 0.5%
small.

## Measure it once

FDM prints are usually off by 0.1 to 0.3 mm. On a 32 mm tag that is up to 1% of scale.
Measure one tag's outer black edge on two faces with calipers and average the
readings. Enter that value as the cube's measured tag size in the app, or pass it as
`--measured-tag-mm` to the pipeline. The pole version (`--bottom socket`) has ticks every 5 mm
on its bottom face as a quick visual check.

## More than one cube

Put down several cubes when one can't be close to everything: along a long crevice, or at the
head, middle and tail of a shark on a deck. Each cube needs its own tag ids so none is ever
mistaken for another. Cubes 0 to 3 are generated already (cube n: tags 5n to 5n+4, and 500+n on
the bottom), and the phone knows all of their tags:

```sh
python3 make_3mf.py --cube-index 2   # calibration-cube-2.3mf
python3 generate.py --cube-index 4   # a fifth cube: tag_bits-4.scad, cube-spec-4.json, stickers-4.svg
                                     # (then python3 swift_codes.py --cubes 5 for the phone)
```

The Mac loads every `cube-spec*.json` here by default, so any of them, or several at once, can be
in the video. The cubes share one scale, each with its own pose, since nobody measures where they
sit relative to each other. Each cube's own scale is checked too: with three or more cubes, one
that disagrees with the rest by more than 1% (misprinted, a wrong caliper reading, knocked
during the sweep) is left out and named; with two, a disagreement is flagged. The model ends up
in the frame of the cube seen best, and `scale.json` lists where every other cube sits in it.
Print all the cubes from the same filament and settings, as one caliper reading applies to all.

## Verification

`python3 -m unittest discover -s tests` renders the `ink` part with OpenSCAD and
ray-casts under every cell of every tag to confirm the print matches `cube-spec.json`
cell for cell. The pipeline's own tests render the cube from several angles and run
the real detector on the renders, which fixes the corner order the solver relies on.

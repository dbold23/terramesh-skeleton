// TerraMesh calibration cube, tiled: a white core and five flat-printed tag tiles.
//
// The one-piece cube prints its four side tags on vertical walls, so every tag edge is a
// stack of layer lines and the side faces come out slightly out of square. Here each tag
// is a thin tile printed face down on the plate, where the printer's X and Y are at their
// sharpest and the face is as flat as the plate. The tiles sit in pockets in the core:
//
//   - Two pins on the back of each tile fit two holes in its own pocket only, and only
//     one way round, so a tile cannot go on the wrong face or turned. The Mac needs to
//     know which tag is on which face and which way up (cube-spec.json).
//   - The pocket is 0.1 mm deeper than the tile. Glue each tile with the cube face down on
//     glass: the tile's face and the pocket's rim both rest on the glass, so the tag ends
//     flush with the cube face whatever the glue does.
//   - The tags sit exactly where the one-piece cube puts them, so the same cube-spec.json,
//     tag codes and pipeline apply.
//
// The bottom stays plain with the 1/4 in dowel socket, printed on the plate. A tag there
// would sit on rock or the pole and never be seen.
//
// Parts (-D 'part="..."'):
//   "core"        white core, socket face down
//   "tiles_body"  the five tiles' white bodies, face down in a row
//   "tiles_ink"   the five tiles' black cells, face down in a row
//   "preview"     the cube assembled, coloured
//   "assembled_ink"  the tiles' black cells in place on the cube (for the spec test)
//   "clash"       where the placed tiles overlap the core; empty when they fit

include <tag_bits.scad>

part = "preview";
edge = GENERATED_EDGE;
cell = GENERATED_CELL;
tag = 8 * cell;

lip = 2.0;               // core rim round each pocket; also the tile thickness limit
pocket = edge - 2 * lip; // 36 mm square
clearance = 0.15;        // per side, tile to pocket wall
tile = pocket - 2 * clearance;
tile_t = 2.0;            // tile thickness, 10 layers at 0.2
pocket_depth = tile_t + 0.1; // room for glue behind a tile pressed flush on glass
ink_depth = 0.6;         // black cells, 3 layers at 0.2, face down on the plate
pin_d = 2.0;
pin_h = 1.0;
hole_d = 2.35;
hole_depth = pin_h + 0.3;
chamfer = 0.8;
socket_d = 6.6;
socket_depth = 18;
gap = 4;                 // between tiles on the plate
eps = 0.01;

assert(tag + 2 < tile, "tile too small for the tag and its white border");
assert(tile_t <= lip, "tiles on neighbouring faces would collide at the cube's edges");

// Where each tag's pins go, in its face frame (x right, y up): one fixed corner pin and one
// along the top edge at a place unique to the tag. No quarter turn of one tag's pins lands
// on another's (or its own) holes, so each tile fits one pocket, one way round.
PIN_X = [-8, -4, 0, 4, 8];
function pins(id) = [[-12, -12], [PIN_X[id % 5], 12]];

module on_face(t) {
    n = t[1]; u = t[2]; w = t[3];
    c = n * edge / 2;
    multmatrix([[u[0], w[0], n[0], c[0]],
                [u[1], w[1], n[1], c[1]],
                [u[2], w[2], n[2], c[2]],
                [0, 0, 0, 1]]) children();
}

// Black cells in a face frame, face at z = 0, cells going into the tile. `grow` keeps
// diagonal neighbours overlapping so the result stays manifold; `lift` extends a cutter
// past the face so the pockets open cleanly.
module black_cells(t, grow = 0.005, lift = 0) {
    bits = t[4];
    for (r = [0 : 7], c = [0 : 7]) if (bits[r][c] == 1)
        translate([-tag / 2 + c * cell - grow, tag / 2 - (r + 1) * cell - grow, -ink_depth])
            cube([cell + 2 * grow, cell + 2 * grow, ink_depth + lift]);
}

// One tile in its face frame: face at z = 0, back at z = -tile_t, pins pointing into the core.
module tile_body(t) {
    difference() {
        translate([-tile / 2, -tile / 2, -tile_t])
            minkowski() {
                translate([0.3, 0.3, 0]) cube([tile - 0.6, tile - 0.6, tile_t - eps]);
                cylinder(r = 0.3, h = eps, $fn = 12);
            }
        black_cells(t, lift = 1);
    }
    for (p = pins(t[0])) translate([p[0], p[1], -tile_t - pin_h]) cylinder(d = pin_d, h = pin_h + eps, $fn = 24);
}

module tile_ink(t) { black_cells(t); }

module chamfered_cube() {
    intersection() {
        cube(edge, center = true);
        rotate([45, 0, 0]) cube([edge, edge * sqrt(2) - chamfer * sqrt(2), edge * sqrt(2) - chamfer * sqrt(2)], center = true);
        rotate([0, 45, 0]) cube([edge * sqrt(2) - chamfer * sqrt(2), edge, edge * sqrt(2) - chamfer * sqrt(2)], center = true);
        rotate([0, 0, 45]) cube([edge * sqrt(2) - chamfer * sqrt(2), edge * sqrt(2) - chamfer * sqrt(2), edge], center = true);
    }
}

module core() {
    difference() {
        chamfered_cube();
        for (t = TAGS) on_face(t) {
            translate([-pocket / 2, -pocket / 2, -pocket_depth]) cube([pocket, pocket, pocket_depth + 1]);
            for (p = pins(t[0])) translate([p[0], p[1], -pocket_depth - hole_depth])
                cylinder(d = hole_d, h = hole_depth + eps, $fn = 24);
        }
        translate([0, 0, -edge / 2 - eps]) cylinder(d = socket_d, h = socket_depth, $fn = 48);
        for (i = [-3 : 3]) translate([i * 5 - 0.3, edge / 2 - 7, -edge / 2 - eps])
            cube([0.6, (i % 2 == 0) ? 4 : 2.5, 0.6]);
    }
}

// Tiles face down on the plate: turned over about x, which keeps the tag readable from
// below (a rotation, not a mirror), then laid out three to a row so they fit a 180 mm bed.
module on_plate(i) {
    translate([(i % 3) * (tile + gap), -floor(i / 3) * (tile + gap), 0]) rotate([180, 0, 0]) children();
}

if (part == "core") core();
else if (part == "tiles_body") for (i = [0 : len(TAGS) - 1]) on_plate(i) tile_body(TAGS[i]);
else if (part == "tiles_ink") for (i = [0 : len(TAGS) - 1]) on_plate(i) tile_ink(TAGS[i]);
else if (part == "assembled_ink") for (t = TAGS) on_face(t) tile_ink(t);
else if (part == "exploded_body") for (t = TAGS) translate(t[1] * 14) on_face(t) tile_body(t);
else if (part == "exploded_ink") for (t = TAGS) translate(t[1] * 14) on_face(t) tile_ink(t);
else if (part == "clash") intersection() { core(); for (t = TAGS) on_face(t) tile_body(t); }
else {
    color("white") core();
    for (t = TAGS) on_face(t) { color("white") tile_body(t); color("black") tile_ink(t); }
}

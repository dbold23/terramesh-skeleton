// TerraMesh intertidal calibration cube
//
// A 40 mm cube with an AprilTag (tag36h11) on every face, or on five faces with a
// handle socket or an anchor (ballast and cord loop) in the sixth (set `bottom`). Placed at the mouth of a crevice, it gives the phone video a known
// metric scale, a fixed origin, and a live check that the camera is close and
// sharp enough. Tag geometry comes from tag_bits.scad, which generate.py writes
// alongside cube-spec.json so the printed cube and the scale solver always agree.
//
// Parts (set `part`, or pass -D 'part="ink"' on the command line):
//   "body"    white body with the black cells recessed as pockets
//   "ink"     the black cells only, to drop into the pockets on a
//             multi-material printer (export both, assign black to "ink")
//   "preview" both together, coloured
//
// Single-extruder printers: print "body" in white and fill the pockets with black
// paint pen or epoxy, or print a plain cube and apply stickers.svg on vinyl.
// Whatever the method, measure the finished tag edge with calipers and enter it
// in the app (it overrides cell_mm * 8 in the scale solve).

include <tag_bits.scad>

part = "preview";        // [body, ink, preview]
bottom = "tag";          // [tag, socket, anchor]: a sixth tag, the 1/4 in dowel socket for a pole,
                         // or the anchor: a sealed ballast pocket and a cord loop, for surge
edge = GENERATED_EDGE;   // cube edge, mm (must match the generator)
cell = GENERATED_CELL;   // tag cell, mm (must match the generator)
inlay_depth = 0.8;       // pocket / ink depth, mm (2 layers at 0.4 or 4 at 0.2)
chamfer = 0.8;           // edge chamfer, stays inside the white quiet zone
socket_d = 6.6;          // fits a 1/4 in (6.35 mm) dowel or a trekking-pole tip adapter
socket_depth = 18;
// Anchor. The pocket is filled with steel shot at a print pause, when the print reaches the
// top of its straight wall (ballast_pause_z, from the plate), before the cone roof closes it.
// Its roof is a 45 degree cone, so nothing inside needs support.
ballast_d = 26;
ballast_floor = 8.5;     // solid under the pocket, holds the cord tunnel
ballast_h = 14.5;        // straight wall; the shot must sit below this
cord_d = 3.4;            // 2-3 mm cord
cord_x = 9;              // the two cord holes, either side of the centre
cord_z = 4.2;            // tunnel centre above the bottom face
ballast_pause_z = ballast_floor + ballast_h;
eps = 0.01;

tag = 8 * cell;
assert(tag + 2 * chamfer < edge, "tag plus chamfer does not fit on the face");

// Local face frame: x along the tag's right edge, y along its up edge, z out.
module on_face(t) {
    n = t[1]; u = t[2]; w = t[3];
    c = n * edge / 2;
    multmatrix([[u[0], w[0], n[0], c[0]],
                [u[1], w[1], n[1], c[1]],
                [u[2], w[2], n[2], c[2]],
                [0, 0, 0, 1]]) children();
}

// `grow` keeps diagonal neighbours overlapping so the result stays manifold;
// `lift` extends a cutter past the surface so pockets open cleanly.
module black_cells(t, grow = 0.005, lift = 0) {
    bits = t[4];
    for (r = [0 : 7], c = [0 : 7]) if (bits[r][c] == 1)
        translate([-tag / 2 + c * cell - grow, tag / 2 - (r + 1) * cell - grow, -inlay_depth])
            cube([cell + 2 * grow, cell + 2 * grow, inlay_depth + lift]);
}

module chamfered_cube() {
    // Intersection of the cube with a cube rotated to cut each edge and corner.
    intersection() {
        cube(edge, center = true);
        rotate([45, 0, 0]) cube([edge, edge * sqrt(2) - chamfer * sqrt(2), edge * sqrt(2) - chamfer * sqrt(2)], center = true);
        rotate([0, 45, 0]) cube([edge * sqrt(2) - chamfer * sqrt(2), edge, edge * sqrt(2) - chamfer * sqrt(2)], center = true);
        rotate([0, 0, 45]) cube([edge * sqrt(2) - chamfer * sqrt(2), edge * sqrt(2) - chamfer * sqrt(2), edge], center = true);
    }
}

module anchor() {
    z0 = -edge / 2;
    // sealed ballast pocket with a self-supporting cone roof
    translate([0, 0, z0 + ballast_floor]) {
        cylinder(d = ballast_d, h = ballast_h, $fn = 64);
        translate([0, 0, ballast_h]) cylinder(d1 = ballast_d, d2 = 0.1, h = ballast_d / 2, $fn = 64);
    }
    // cord loop: two holes up from the bottom face, joined by a tunnel with a pointed
    // (teardrop) roof that prints without support
    for (x = [-cord_x, cord_x]) {
        translate([x, 0, z0 - eps]) cylinder(d = cord_d, h = cord_z + eps, $fn = 24);
        translate([x, 0, z0 - eps]) cylinder(d1 = cord_d + 2, d2 = cord_d, h = 1, $fn = 24);  // eased mouth
    }
    r = cord_d / 2;
    translate([-cord_x, 0, z0 + cord_z]) rotate([0, 90, 0]) {  // local -x is world up
        cylinder(r = r, h = 2 * cord_x, $fn = 24);
        linear_extrude(2 * cord_x) polygon([[-r * sqrt(2), 0], [-r / sqrt(2), r / sqrt(2)], [-r / sqrt(2), -r / sqrt(2)]]);
    }
    for (x = [-cord_x, cord_x]) translate([x, 0, z0 + cord_z]) sphere(d = cord_d, $fn = 24);
}

module body() {
    difference() {
        chamfered_cube();
        for (t = TAGS) on_face(t) black_cells(t, lift = 1);
        if (bottom == "tag") {
            on_face(BOTTOM_TAG) black_cells(BOTTOM_TAG, lift = 1);
        } else {
            if (bottom == "anchor") anchor();
            // handle socket in the untagged bottom face
            else translate([0, 0, -edge / 2 - eps]) cylinder(d = socket_d, h = socket_depth, $fn = 48);
            // bottom-face scale ticks every 5 mm, a manual check of print scale
            for (i = [-3 : 3]) translate([i * 5 - 0.3, edge / 2 - 7, -edge / 2 - eps])
                cube([0.6, (i % 2 == 0) ? 4 : 2.5, 0.6]);
        }
    }
}

module ink() {
    for (t = TAGS) on_face(t) black_cells(t);
    if (bottom == "tag") on_face(BOTTOM_TAG) black_cells(BOTTOM_TAG);
}

if (part == "body") body();
else if (part == "ink") ink();
else { color("white") body(); color("black") ink(); }

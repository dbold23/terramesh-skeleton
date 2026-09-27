// TerraMesh Field Cube v1 -- units: mm. Original mechanical design, CC BY 4.0.
// Prototype: physical fit, impact strength and survey accuracy require testing.
// Render: openscad -o body.stl -D 'part="body"' field_cube.scad
include <markers.scad>;
$fn=32;
part="assembly";
tag_id=0;
S=112; H=106; lid_h=6; wall=5; floor_h=6;
tile=84; pocket=84.6; pocket_depth=2; base_h=1.2; ink_h=0.4;
post=16; post_xy=46; bolt_d=4.5; nut_af=7.5; nut_h=3.5;
// One offset screw prevents rotating the lid relative to the calibrated faces.
bolt_positions=[[-46,-46],[46,-46],[-46,46],[47.5,46]];
cuff_h=17; cuff_floor=5;

module rr(w,h,r=3) { offset(r=r) square([w-2*r,h-2*r],center=true); }
module outer_body() {
  // Small 45-degree first-layer chamfer, no large downward-facing recess.
  hull() {
    linear_extrude(0.01) rr(S-1.6,S-1.6,2.2);
    translate([0,0,0.8]) linear_extrude(0.01) rr(S,S,3);
  }
  translate([0,0,0.8]) linear_extrude(H-0.8) rr(S,S,3);
}
// Local face +u points right and +v up when viewed from outside.
module face(i) {
  if(i==0) multmatrix([[1,0,0,0],[0,0,-1,-56],[0,1,0,56],[0,0,0,1]]) children();
  if(i==1) multmatrix([[0,0,1,56],[1,0,0,0],[0,1,0,56],[0,0,0,1]]) children();
  if(i==2) multmatrix([[-1,0,0,0],[0,0,1,56],[0,1,0,56],[0,0,0,1]]) children();
  if(i==3) multmatrix([[0,0,-1,-56],[-1,0,0,0],[0,1,0,56],[0,0,0,1]]) children();
  if(i==4) translate([0,0,112]) children();
  if(i==5) multmatrix([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]]) children();
}
module pocket_cut() { translate([0,0,-2]) linear_extrude(2.1) rr(pocket,pocket,1.3); }
module nut_slot(x,y,z=98.5) {
  translate([x,y,z]) rotate([0,0,30]) cylinder(h=nut_h,r=nut_af/sqrt(3),$fn=6);
  translate([x,y-sign(y)*8,z+nut_h/2]) cube([nut_af,16,nut_h],center=true);
}
module body() {
 difference() {
  union() {
   difference() {
    outer_body();
    translate([0,0,floor_h]) linear_extrude(H+1) rr(S-2*wall,S-2*wall,3);
   }
   for(x=[-post_xy,post_xy],y=[-post_xy,post_xy])
     translate([x-post/2,y-post/2,0.8]) cube([post,post,H-0.8]);
  }
  for(i=[0:3]) face(i) pocket_cut();
  for(p=bolt_positions) let(x=p[0],y=p[1]) {
   translate([x,y,91]) cylinder(d=bolt_d,h=H-91+1);
   nut_slot(x,y);
  }
  // Cord runs diagonally through reinforced +X/+Y bottom corner.
  translate([51,51,24]) rotate([90,0,45]) cylinder(d=5,h=50,center=true);
  for(p=[[56,46,24],[46,56,24]]) translate(p) sphere(d=6.4);
  // TPU cuff beads latch into these shallow, non-fiducial grooves.
  for(z=[7,103]) translate([0,0,z]) linear_extrude(2)
    difference() { square([120,120],center=true); rr(110.8,110.8,2.4); }
  // Bottom drainage outside the 84 mm tile.
  for(p=[[48,0],[-48,0],[0,48],[0,-48]])
    translate([p[0],p[1],-0.1]) cylinder(d=3,h=floor_h+0.2);
 }
}
module lid() {
 difference() {
  linear_extrude(lid_h) rr(S,S,3);
  translate([0,0,lid_h]) pocket_cut();
  for(p=bolt_positions) let(x=p[0],y=p[1]) {
   translate([x,y,-0.1]) cylinder(d=bolt_d,h=lid_h+0.2);
   translate([x,y,lid_h-3]) cylinder(d=9,h=3.1);
  }
 }
}
module cuff() {
 difference() {
  union() {
   linear_extrude(cuff_floor) difference() { rr(120,120,7); square([96,96],center=true); }
   translate([0,0,cuff_floor]) linear_extrude(cuff_h-cuff_floor)
     difference() { rr(120,120,7); rr(112.4,112.4,3.2); }
   // Elastic registration bead: 0.2 mm radial clearance in the core groove.
   translate([0,0,12]) linear_extrude(2)
     difference() { rr(120,120,7); rr(111.2,111.2,2.6); }
  }
  // M4 head/driver access; flexible armor is outside the structural fastener stack.
  for(p=bolt_positions)
   translate([p[0],p[1],-0.1]) cylinder(d=12,h=cuff_floor+0.2);
  for(p=[[48,0],[-48,0],[0,48],[0,-48]])
   translate([p[0],p[1],-0.1]) cylinder(d=4,h=cuff_floor+0.2);
 }
}
module blank_tile() {
 linear_extrude(base_h) difference() {
  rr(tile,tile,1);
  translate([-1.5,tile/2-0.6]) square([3,0.7]);
 }
}
module marker_tile(id) {
 union() { blank_tile(); field_cube_marker_black(id,z_base=base_h,height=ink_h); }
}
module fit_coupon() {
 difference() {
  cube([96,28,8]);
  // A full-width shallow channel tests the 84 mm tile fit and 2 mm recess.
  translate([5.7,-0.1,6]) cube([pocket,15.1,2.1]);
  translate([18,22,-0.1]) cylinder(d=2.6,h=8.2);
  translate([36,22,-0.1]) cylinder(d=4.5,h=8.2);
  translate([54,22,4.5]) rotate([0,0,30]) cylinder(r=nut_af/sqrt(3),h=3.6,$fn=6);
  translate([54,22,-0.1]) cylinder(d=4.5,h=8.2);
  translate([78,22,-0.1]) cylinder(d=5,h=8.2);
 }
}
module tile_strip() { cube([84,12,1.6]); }
module cuff_fit_clip() {
 // 36 mm section of the real TPU side rail, including the retention bead.
 intersection() { cuff(); translate([-18,-61,0]) cube([36,10,cuff_h]); }
}
module core_fit_rail() {
 difference() {
  cube([36,8,12]);
  translate([-0.1,-0.1,7]) cube([36.2,0.7,2]);
 }
}
module assembly(explode=0) {
 color([0.98,0.29,0.06]) body();
 color([0.98,0.29,0.06]) translate([0,0,H+explode]) lid();
 color([0.12,0.16,0.17]) translate([0,0,-5-explode]) cuff();
 color([0.12,0.16,0.17]) translate([0,0,117+2*explode]) rotate([180,0,0]) cuff();
 for(i=[0:5]) face(i) translate([0,0,(i==5?0:-2)+explode]) {
  color("white") blank_tile();
  color([0.02,0.02,0.02]) field_cube_marker_black(i,z_base=base_h,height=ink_h);
 }
}

if(part=="body") body();
else if(part=="lid") lid();
else if(part=="cuff") cuff();
else if(part=="tile") marker_tile(tag_id);
else if(part=="blank_tile") blank_tile();
else if(part=="fit_coupon") fit_coupon();
else if(part=="tile_strip") tile_strip();
else if(part=="cuff_fit_clip") cuff_fit_clip();
else if(part=="core_fit_rail") core_fit_rail();
else if(part=="exploded") assembly(25);
else assembly();

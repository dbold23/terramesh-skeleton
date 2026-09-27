# TerraMesh

Walk a site with an iPhone, get a 3D habitat map with every photographed organism placed
in it, then refine it afterwards on a Mac or a field station.

> **Skeleton of an ongoing project.** This covers the planned architecture, the
> photogrammetry and the post-capture station workers: real module layout, signatures and
> docstrings, with every function body replaced by `...`. The iPhone app, footage, models
> and site data are left out. It does not run, but the plan and the docstrings are enough
> to build your own. You are welcome to; please credit Daniel Sambold if you do.

<img src="docs/curb-preview.png" width="100%" alt="Textured reconstruction of a curb and plants from one iPhone video">

<sub>First real-video test: one curb clip, 163 frames, all registered by Apple's native
photogrammetry into a textured preview (12,540 vertices). Metric scale and geographic
alignment are not yet verified.</sub>

## The plan

[`docs/architecture.md`](docs/architecture.md) is the design: SwiftUI, ARKit, Core
Location, Vision and Core ML, RealityKit. ARKit's visual-inertial tracking gives a metric
local route (no double-integrating the accelerometer); LiDAR depth places an observation
directly when it exists, and multiple viewpoints triangulate it when it does not. The
first deliverable is a walk trajectory with clickable 3D observations and their evidence;
full textured surfaces come later, off the phone. Links in it to the app code point at
parts that are not in this skeleton.

## Build your own

1. **Capture.** Save sharp, overlapping stills with their ARKit camera poses, GPS fixes
   and optional depth, as an evidence package rather than a movie.
2. **Sparse reconstruction.** Extract upright SDR frames, run COLMAP for cameras and a
   sparse cloud, and audit it: registered frames, disconnected models, residuals
   (`photogrammetry/run_sparse.py`, `analyze_sparse.py`).
3. **Dense surface.** Request a textured mesh from a second engine and treat it as an
   independent reconstruction, never in COLMAP's frame (`photogrammetry/native/`).
4. **Register the layers.** Fit a similarity between camera-centre sets to put every
   layer in one site frame, and record how well it fits (`register_twin.py`,
   `twinlib/similarity.py`, `twinlib/arkit.py`).
5. **Scale.** Put a printed calibration cube or scale bar in the scene; detect its markers
   and solve the scale (`photogrammetry/intertidal/intertidal/cube.py`, `scale.py`).
6. **Measure and publish.** Intertidal crevice measurements, waterline and tide context,
   then a Darwin Core Archive (`intertidal/measure.py`, `export_dwc.py`, `twinlib/dwc.py`).
7. **Post-process on a station.** Workers re-rank photo IDs, score recorded sound and
   shortlist known individuals for a human to confirm (`station/workers/`).

## Layout

| Part | What it holds |
|---|---|
| `photogrammetry/twinlib/` | The twin package format (`SCHEMA.md`): COLMAP, ARKit, PLY, Earth alignment, audit |
| `photogrammetry/intertidal/` | Cube-scaled intertidal reconstruction and crevice measurement |
| `photogrammetry/*.py` | Sparse runs, twin build and registration, SAM 3 cataloguing, DwC export |
| `photogrammetry/native/` | The Apple photogrammetry wrapper (Swift, not included) |
| `station/vault/` | One verified, deduplicated copy of every survey the phone sends |
| `station/workers/audio-id/` | Perch 2.0 and BirdNET scoring of recorded sound |
| `station/workers/bioclip-rerank/` | BioCLIP re-ranking of photographed observations |
| `station/workers/individual-match/`, `shark-match/` | Shortlists of known individuals for a reviewer |
| `station/workers/intertidal-recon/`, `shark-morphometrics/` | Scaled reconstruction and measurement jobs |

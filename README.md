# TerraMesh

Walk a site with an iPhone, get a 3D habitat map with every photographed organism placed
in it, then refine it afterwards on a Mac or a field station.

> **Skeleton of an ongoing project.** This covers the planned architecture, the
> photogrammetry and the post-capture station workers: real module layout, signatures and
> docstrings, with every function body replaced by `...`. The iPhone app, footage, models
> and site data are left out. It does not run, but the plan and the docstrings are enough
> to build your own. You are welcome to; please credit Daniel Sambold if you do.

## Collaborate

I am looking for collaborators. What needs work:

- **Field accuracy.** Metric scale, geographic alignment and surface accuracy are not yet verified in the field; the cube-scaling gates need real site tests.
- **On-device testing** across iPhones, with and without LiDAR.
- **Planned pieces not built yet:** GBIF publishing, offsite mirroring and Wi-Fi sync.
- **Intertidal and cave sites**, and partners who survey them.

<p>
  <a href="https://github.com/dbold23/terramesh-skeleton/issues/new?template=1-collaborate.yml"><img alt="Propose a collaboration" src="https://img.shields.io/badge/Propose%20a%20collaboration-0b1f33?style=for-the-badge&labelColor=2bb3a9&color=2bb3a9"></a>
  <a href="https://github.com/dbold23/terramesh-skeleton/issues/new?template=2-beta-tester.yml"><img alt="Become a beta tester" src="https://img.shields.io/badge/Become%20a%20beta%20tester-0b1f33?style=for-the-badge&labelColor=f2a93b&color=f2a93b"></a>
  <a href="https://github.com/dbold23/terramesh-skeleton/issues/new?template=3-share-data.yml"><img alt="Share data or a site" src="https://img.shields.io/badge/Share%20data%20or%20a%20site-0b1f33?style=for-the-badge&labelColor=2bb3a9&color=2bb3a9"></a>
  <a href="mailto:daniel.sambold@gmail.com?subject=About%20TerraMesh"><img alt="Email me" src="https://img.shields.io/badge/Email%20me-daniel.sambold%40gmail.com-0b1f33?style=for-the-badge&labelColor=f2a93b&logo=gmail&logoColor=0b1f33"></a>
</p>

<sub>Beta testing needs an iPhone (LiDAR Pro models help most, but any recent iPhone is useful); I reply on the issue with next steps. The first buttons open a short public form (needs a GitHub account). No account, or rather keep it private? Email <a href="mailto:daniel.sambold@gmail.com">daniel.sambold@gmail.com</a> or message me on <a href="https://www.linkedin.com/in/daniel-sambold-620b37221">LinkedIn</a>.</sub>

<img src="docs/curb-preview.png" width="100%" alt="Textured reconstruction of a curb and plants from one iPhone video">

<sub>First real-video test: one curb clip, 163 frames, all registered by Apple's native
photogrammetry into a textured preview (12,540 vertices). Metric scale and geographic
alignment are not yet verified.</sub>

<img src="docs/abalone-cave.gif" width="100%" alt="An abalone cave scanned with an iPhone and rebuilt in 3D">

<sub>A newer scan: an abalone cave, 23 September.</sub>

## Where it stands

- **Works today:** phone capture with ARKit poses and a signed evidence ledger; COLMAP and
  OpenMVS reconstruction on a Mac station (10.7 million dense points on the abalone cave);
  printed AprilTag cubes that set the scale; coverage maps and crevice metrics.
- **Not yet verified:** metric scale, geographic alignment and surface accuracy in the
  field. Treat every number here as a lab result until the field tests are done.
- **Planned, not built:** GBIF publishing, offsite mirroring and Wi-Fi sync (dashed below).

## Architecture now

```mermaid
flowchart LR
  classDef planned stroke-dasharray: 5 5,opacity:0.8
  subgraph Phone["iPhone: capture"]
    AR["ARKit poses<br/>+ LiDAR depth"] --> REC["Survey recorder<br/>stills · 45 s sweeps · sound"]
    GUIDE["Live guides<br/>cube tag reader · crevice coverage · blur check"] --> REC
    REC --> LED["Signed ledger + seal<br/>Secure Enclave ES256"]
  end
  subgraph Station["Mac Station: archive + compute"]
    VAULT[("Vault<br/>SHA-256 named, read-only")]
    PG["Photogrammetry<br/>ALIKED + LightGlue → COLMAP (ARKit priors)<br/>→ cube scale → OpenMVS dense"]
    MET["mm models · crevice metrics<br/>coverage · tide heights"]
    WK["uv workers<br/>audio ID · shark re-ID · BioCLIP"]
    VER["Verify + C2PA credentials"]
    VAULT --> PG --> MET
    VAULT --> WK
    VAULT --> VER
  end
  subgraph Cloud["Public"]
    R2["R2: web-sized derivatives<br/>WebP · Draco / 3D Tiles"]
    GBIF["GBIF publishing"]:::planned
  end
  LED -- "export ZIP" --> VAULT
  VAULT -. "receipts → Free up" .-> REC
  MET --> R2
  WK --> R2
  MET --> GBIF
  VAULT -.-> MIR[("Mirror drive → R2 offsite")]:::planned
  REC -.-> WIFI["Wi-Fi sync (Bonjour)"]:::planned
```

<sub>Dashed boxes are planned, not built. Drawn from the current docs on 27 September.
[`docs/architecture.md`](docs/architecture.md) is the original 10 September design it grew
from (SwiftUI, ARKit, Core Location, Vision and Core ML, RealityKit; ARKit's visual-inertial
tracking for a metric route, LiDAR or multiple viewpoints to place an observation). Parts it
mentions, such as the app code, are not in this skeleton.</sub>

## Photogrammetry, stage by stage

<img src="docs/pipeline-stages.gif" width="100%" alt="The abalone cave at each stage: sparse points, dense cloud, mesh, textured model">

<sub>The 23 September abalone cave from one fixed camera: COLMAP sparse points, the OpenMVS
dense cloud (10.7 million points), the cleaned millimetre mesh, and the textured model.</sub>

```mermaid
flowchart LR
  V["Phone sweep<br/>video + ARKit poses"] --> F["Frames"]
  C["Calibration cube<br/>AprilTags"] --> S
  F --> M["ALIKED + LightGlue<br/>features & matches"] --> SP["COLMAP 4.2<br/>sparse, pose priors"]
  SP --> S["Cube scale<br/>→ millimetres"] --> D["OpenMVS<br/>dense cloud"] --> ME["Mesh + photo texture"]
  ME --> K["Crevice metrics<br/>width · height · depth · seen %"]
  ME --> T["Tide heights"]
```

## Post-processing

<table>
<tr>
<td width="50%"><img src="docs/post/tag-detections.jpg" width="100%" alt="Phone still with the calibration cube's AprilTags detected"></td>
<td width="50%"><img src="docs/post/cube-detection.png" width="100%" alt="Cube and tag positions located on the dense cloud"></td>
</tr>
<tr>
<td align="center"><sub>AprilTags found on the calibration cube</sub></td>
<td align="center"><sub>The cube located on the dense cloud: this sets the scale</sub></td>
</tr>
<tr>
<td><img src="docs/post/camera-path.png" width="100%" alt="Camera path of the registered stills"></td>
<td><img src="docs/post/coverage.png" width="100%" alt="Surface coverage map"></td>
</tr>
<tr>
<td align="center"><sub>Where every registered still was taken</sub></td>
<td align="center"><sub>How well each part of the surface was seen</sub></td>
</tr>
</table>

<img src="docs/post/desk-model.jpg" width="100%" alt="The final textured model from four sides">

<sub>The finished model from four sides (desk-cube test, 25 September).</sub>

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
5. **Scale.** Print a calibration cube (`hardware/`, 3MFs ready to slice) and put it in the scene; detect its markers
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
| `hardware/calibration-cube/`, `hardware/field-cube/` | The printed AprilTag scale cubes: OpenSCAD sources, STLs, tag artwork and print notes (generator scripts as skeletons) |
| `hardware/3mf/` | Ready-to-print 3MF files: the 40 mm six-tag cube, numbered cubes 1 to 3, the tiled plate and cube 3 keyed |

## Cite

If this helps your work, please credit Daniel Sambold. GitHub's "Cite this repository" button (from `CITATION.cff`) gives the citation in APA or BibTeX.

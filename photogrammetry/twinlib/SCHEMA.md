# TerraMesh twin package, format 1

A twin package is a folder that a browser viewer reads and a Python builder writes. It joins one
place ("site") across visits: phone survey exports and Mac photogrammetry runs. The builder never
writes into a survey export. The viewer never writes anything except append-only journals through
the local server. Every position in a layer file is in that layer's own frame; the viewer applies
the transform recorded in `transforms.json`. Nothing in the package promotes a number above the
claim level it arrived with.

```
twin/<site-id>/
  twin.json                    manifest (written last, atomically)
  transforms.json              layer frame -> site frame records
  control-points.jsonl         append-only, operator-declared stable control
  anchors.jsonl                append-only, last revision per id wins
  tags.jsonl                   append-only, last revision per id wins
  audit.jsonl                  append-only, hash-chained
  visits/<visit-id>/
    visit.json
    layers/
      splat/          layer.json  splat-lod1.ply          (3DGS PLY, DC colour only, subsampled)
      mesh/           layer.json  mesh.obj mesh.mtl tex0.png
      sparse/<piece>/ layer.json  points.ply              (binary little-endian: float x y z, uchar red green blue)
      stations/       layer.json  stations.json  thumbs/<station-id>.jpg
      observations/   layer.json  observations.json  images/<frame-id>.jpg   (evidence copies, 1024 px max)
      coverage/       layer.json  patches.json
      measurements/   layer.json  measurements.json
      joins/          layer.json  joins.json
      clips/          layer.json  clips.json  media/<clip-id>.<ext>
  cache/                       regenerable; never authoritative
```

## Frames and axes

- Layer frames are named `visits/<visit-id>/layers/<kind>[/<sub>]` and the site frame is `site`.
- Matrices are 16 numbers, **column-major**, `[x', y', z', 1] = M · [x, y, z, 1]`, same convention as
  ARKit `cameraTransform` and `earth-placement.json`.
- `site.frame.kind == "enu_metric"`: axes `["east", "north", "up"]`, units metres, origin at
  `site.anchor` (WGS84) at the anchoring segment's reference position height. The viewer converts
  ENU to its Y-up scene with the fixed rotation x=east, y=up, z=south (`z = -north`).
- `site.frame.kind == "local_unscaled"`: axes `["x", "y", "z"]` of the pinned layer, Y assumed up,
  units `"unscaled"` unless `scale_status` says otherwise. No length may be printed as metres.
- ARKit segment frames are metric, Y up, initial camera forward −Z. COLMAP frames are arbitrary
  scale; camera-to-world for image i is the inverse of `[R_cw | t_cw]`. RealityKit local frames are
  Y up with unverified scale.

## twin.json

```json
{
  "format": "TerraMesh twin package 1", "schema_version": 1,
  "builder": {"name": "build_twin.py", "version": "1"}, "built_at": "2026-09-17T20:00:00Z",
  "site": {
    "id": "curb", "name": "Curb walk", "created_at": "...",
    "anchor": {"latitude": 36.6, "longitude": -121.9, "source": "visit:<id>/segment:<uuid>"} | null,
    "frame": {"kind": "enu_metric" | "local_unscaled", "axes": ["east","north","up"] | ["x","y","z"],
              "units": "metres" | "unscaled", "pinned_layer": null | "<layer-id>",
              "scale_status": "metric" | "unverified" | "unknown",
              "vertical_note": "Up is relative to the anchoring segment's reference position; heights across segments and visits are not commensurable."},
    "default_visit": "<visit-id>"
  },
  "visits": [{"id": "...", "path": "visits/<id>", "date": "YYYY-MM-DD", "kind": "survey_export" | "reconstruction_run" | "both",
              "survey_id": null | "<uuid>", "run_id": null | "<name>", "mission": null | "biodiversity",
              "registration_state": "registered" | "partial" | "unregistered"}],
  "layers": [{"id": "visits/<v>/layers/mesh", "visit_id": "<v>", "kind": "mesh", "path": "visits/<v>/layers/mesh",
              "frame_id": "visits/<v>/layers/mesh" | "<other layer id>", "version": 1,
              "claim": "evidence" | "derived_view", "counts": {...}, "bytes": 123, "sha256": "...",
              "transform_id": "t-..." | null}],
  "integrity": {"audit_event_count": 12, "audit_head_hash": "..."}
}
```

Layer kinds: `splat`, `mesh`, `sparse`, `stations`, `observations`, `coverage`, `measurements`,
`joins`, `clips`. `sparse`, `stations`, `observations` are `evidence`; `splat`, `mesh`, `coverage`
are `derived_view`; the rest are `record`. A layer whose `frame_id` names another layer shares that
layer's transform (the curb-02 splat was trained on COLMAP piece 2, so its `frame_id` is the
`sparse/2` layer id).

## layer.json (beside every layer)

```json
{"id": "...", "visit_id": "...", "kind": "mesh", "frame_id": "...", "version": 1,
 "claim": "derived_view", "producer": {"name": "RealityKit.PhotogrammetrySession", "version": "preview"},
 "source_sha256": ["..."], "original_path": "/abs/path/model.usdz" | null,
 "counts": {"vertices": 12540, "faces": 25000}, "caveats": ["Derived view, not a measured surface."]}
```

Splat layers add `full_point_count`, `lod_point_count`, `selection_method`, `dropped_fields`.

## Viewer-facing layer files

**stations/stations.json** — from `frames.jsonl` (export) or run poses.
```json
{"frame_id": "visits/<v>/layers/stations", "count": 163,
 "stations": [{"id": "<frame uuid or image name>", "image_name": "frame_000001.jpg" | "<uuid>.jpg",
   "timestamp": 12.34, "captured_at": "..." | null, "segment_id": "<uuid>" | null,
   "camera_to_world_column_major": [16], "fx": 1612.7, "fy": 1612.7, "cx": 540, "cy": 960,
   "width": 1080, "height": 1920, "tracking_state": "normal" | null, "capture_reason": "translation" | null,
   "thumb": "thumbs/<id>.jpg", "image": "relative path inside the package" | null}]}
```
`camera_to_world` follows the ARKit convention: camera looks down its −Z, +Y up, +X right, in the
layer frame. Builders convert COLMAP (OpenCV: +Z forward, −Y up) with a 180° rotation about X.

**observations/observations.json** — from `manifest.json`.
```json
{"frame_id": "visits/<v>/layers/observations", "observations": [{
  "id": "<uuid>", "created_at": "...", "label": "…", "notes": "…", "segment_id": "<uuid>",
  "position": [x, y, z] | null, "placement": "pending" | "depth" | "triangulated", "geometric_residual_m": null | 0.03,
  "identification": {"taxon_name": "...", "rank": "species", "status": "suggested" | "confirmed" | "...", "model_identifier": "..."} | null,
  "life_state": null | "living" | "dead" | "unknown", "persistence": null | "...", "catalog_role": null | "anchor" | "...",
  "export_prior": {"review_status": null | "...", "verification": null | {...}},
  "evidence": [{"frame_id": "<uuid>", "image": "images/<uuid>.jpg" | null, "pixel_x": 0.0, "pixel_y": 0.0,
                "depth_m": null | 1.2, "identification": {...} | null}],
  "measurement_ids": ["<uuid>"], "contact_hazard": null | {"probability": 0.9, "taxon": "..."}
}]}
```
The viewer draws a pin only when `position` is non-null and `placement != "pending"`.

**coverage/patches.json** — rebuilt from `sparse-points.jsonl`.
```json
{"frame_id": "...", "cell_size_m": 0.5, "elevation_band_m": 1.0, "source": "sparse-points.jsonl (max revision per identifier)",
 "patches": [{"x": -3, "z": 7, "band": 0, "point_count": 12, "supported_count": 9, "viewpoint_max": 4}]}
```

**measurements/measurements.json** — `ObservationMeasurement` records verbatim with snake_case keys
(`id, kind, value, unit, uncertainty, claim_level, method, method_version, model_identifier,
window_seconds, sample_count, started_at, source_frame_ids, source_clip_id, camera_pose,
spatial_scope, joined_context_id, unsupported_reason, segment_id, mission, notes`).

**joins/joins.json** — `JoinedContext` records verbatim (snake_case).

**clips/clips.json** — `TimedClipRecord` records verbatim plus `media` relative path.

## transforms.json

```json
{"format": "TerraMesh twin transforms 1", "schema_version": 1, "site_frame_id": "site",
 "transforms": [{
   "id": "t-<uuid>", "from_frame": "<layer id>", "to_frame": "site",
   "matrix_column_major": [16] | null, "scale": 1.0 | null,
   "state": "registered" | "prior" | "declared" | "unregistered",
   "method": "umeyama_ransac" | "earth_placement" | "control_points" | "icp" | "enu_prior" | "identity_pin" | "none",
   "method_version": "register_twin/1",
   "matched_count": 0, "inlier_count": 0, "rejected_count": 0,
   "rmse_m": null | 0.08, "median_err_m": null, "max_err_m": null, "rmse_pct_of_reference_path": null,
   "uncertainty_m": null | 0.09, "scale_source": "arkit_similarity" | "earth_placement" | "none",
   "units": "metres" | "unscaled", "vertical_state": "resolved" | "unresolved",
   "inputs": [{"layer_id": "...", "sha256": "..."}],
   "computed_by": {"tool": "register_twin.py", "version": "1", "host": "..."}, "computed_at": "...",
   "unsupported_reason": null | "...", "caveats": ["..."]}]}
```
Rules: `state == "registered"` requires a matrix and a non-null `rmse_m`; `state == "unregistered"`
requires `matrix_column_major == null` and a non-empty `unsupported_reason`; `identity_pin` is the
one transform that pins a `local_unscaled` site to a layer (matrix = identity, state `declared`).

## Journals

All `*.jsonl` files hold one JSON object per line, UTF-8, `\n` terminated, appended only.

**anchors.jsonl**
```json
{"id": "a-<uuid>", "revision": 1, "created_at": "...", "author_ref": "<audit event id>",
 "visit_id": "...", "layer_id": "...", "layer_version": 1,
 "kind": "point" | "barycentric" | "splat_region",
 "site_position": [x, y, z] | null, "frame_local_position": [x, y, z], "transform_id": "t-..." | null,
 "registration_state": "registered" | "prior" | "declared" | "unregistered",
 "radius_m": null | 0.2, "normal": [x, y, z] | null, "normal_confidence": "high" | "low" | null,
 "barycentric": null | {"mesh_layer_id": "...", "mesh_version": 1, "triangle_index": 0, "u": 0.3, "v": 0.2},
 "on_derived_view": true | false,
 "evidence": [{"observation_id": "...", "frame_id": "...", "image_path": "...", "pixel_x": 0, "pixel_y": 0}],
 "source_observation_id": null | "<uuid>", "label": "...", "notes": "", "retracted": false}
```
`site_position` must be null unless `registration_state == "registered"`.

**tags.jsonl**
```json
{"id": "g-<uuid>", "revision": 1, "created_at": "...", "author_ref": "...", "name": "colony 3",
 "taxon": null | {"name": "...", "rank": "...", "gbif_key": null},
 "tag_kind": "temporal_track",
 "members": [{"visit_id": "...", "anchor_id": "...", "added_at": "...",
              "match": {"method": "operator_visual" | "control_point_proximity" | "same_observation_id",
                        "confidence": "asserted" | "probable" | "uncertain",
                        "separation_m": null | 0.1, "registration_uncertainty_m": null | 0.05}}],
 "identity_claim": "none", "retracted": false}
```
`identity_claim` must be the string `"none"`.

**control-points.jsonl**
```json
{"id": "cp-<uuid>", "created_at": "...", "author_ref": "...", "label": "stair nosing NE",
 "pairs": [{"visit_id": "...", "anchor_id": "..."}], "retired": false}
```

**audit.jsonl**
```json
{"id": "e-<uuid>", "seq": 0, "at": "2026-09-17T20:00:00.000Z",
 "author": {"name": "Daniel", "email": null, "device": "mac-m4", "agent": "builder" | "viewer"},
 "action": "package.created", "target": {"kind": "package", "id": "curb", "visit_id": null},
 "payload": {}, "prev_hash": "000…0 (64 zeros)", "hash": "<sha256 hex>"}
```
Canonical bytes for hashing: `json.dumps(event_without_hash, sort_keys=True, separators=(",", ":"),
ensure_ascii=False).encode("utf-8")`; `hash = sha256(canonical).hexdigest()`. `prev_hash` is the
previous line's `hash`. A verifier re-walks the file and reports the first bad `seq`. Actions:
`package.created, visit.added, layer.added, transform.computed, anchor.created, anchor.moved,
anchor.retracted, tag.created, tag.member.added, tag.member.removed, tag.retracted,
control_point.declared, control_point.retired, review.recorded, note.added`.

`review.recorded` payload: `{"subject_visible": ..., "date_accurate": ..., "location_accurate": ...,
"human_identification": "...", "notes": "...", "prior": {"source": "export", "review_status": ...,
"verification": ..., "author": "unknown"}}`. The effective review status of an observation is a fold
over these events seeded by `observations.json[].export_prior`, computed at read time.

## Local server contract (`twin-viewer/serve.py`)

- `GET /` → viewer; `GET /pkg/<path>` → files under the package root only (realpath containment).
- `POST /events` body `{"author": {...}, "action": "...", "target": {...}, "payload": {...},
  "client_time": "..."}` → server assigns `id`, `seq`, `at`, `prev_hash`, `hash` under a file lock and
  returns `{"seq": n, "hash": "...", "prev_hash": "..."}`. Allowlisted actions only; 64 KB body cap;
  `--read-only` returns 403.
- `POST /journal/<anchors|tags|control-points>` body = one record → appended verbatim after schema
  validation; returns `{"ok": true}`. The viewer always posts the audit event first, then the record.

## Python API (`photogrammetry/twinlib`)

```python
twinlib.ply.read_header(path) -> PlyHeader            # .vertex_count, .properties [(name, dtype)], .data_offset, .little_endian
twinlib.ply.iter_vertices(path, chunk=200_000)        # yields numpy structured arrays
twinlib.ply.write_binary(path, array)                 # structured array -> binary_little_endian PLY
twinlib.similarity.umeyama(src, dst, with_scale=True) -> (s, R, t)
twinlib.similarity.fit_ransac(src, dst, threshold, iterations=500, with_scale=True, seed=0) -> FitResult
twinlib.earth.east_north(lat, lon, ref_lat, ref_lon) -> (e, n)   # port of GeographicAlignment.eastNorth
twinlib.audit.append_event(path, event: dict) -> dict            # assigns seq/prev_hash/hash; locked; fsync
twinlib.audit.verify_chain(path) -> ChainReport                   # .ok .length .head_hash .first_bad_seq
twinlib.schema.validate_package(root) -> list[str]                # [] when valid
twinlib.schema.validate_record(kind, record) -> list[str]         # kind in anchor|tag|control_point|event
```

## Schema notes

Changes and clarifications the Python side needed while implementing this contract. Every one is
additive: no field named above was renamed or removed, and a viewer written against the sections
above still reads a package written by `build_twin.py`.

1. **`transforms[].scale_source` gains `"realitykit_similarity"`.** The enum in the transforms
   section reads `"arkit_similarity" | "earth_placement" | "none"`. A run with no phone export
   behind it (curb-02) can only be registered against RealityKit's estimated local frame, whose
   scale nothing has verified, and calling that `arkit_similarity` would be a lie. The full enum is
   now `"arkit_similarity" | "realitykit_similarity" | "earth_placement" | "none"`. A
   `realitykit_similarity` transform always has `units: "unscaled"`, and the viewer must treat it
   exactly as it treats an unscaled frame: no length may be printed as metres.

2. **`rmse_m`, `median_err_m`, `max_err_m` and `uncertainty_m` are in the target frame's units, not
   always metres.** The field names say metres because the common case is metres. When
   `units == "unscaled"` these residuals are in that frame's own arbitrary units; the transform
   carries the caveat "rmse_m is expressed in this frame's own unscaled units, not metres." The
   viewer must read `units` before it prints a unit beside any of these four numbers. Renaming the
   fields would have broken the viewer being written against this file, so the rule is written down
   here instead.

3. **`stations[].tracking_state` is lowercased.** The export writes ARKit's own spellings —
   `"Normal"`, `"Initialising"`, `"Limited: motion"`, `"Relocalising"` — and `SurveyStore` itself
   compares them case-insensitively. The builder lowercases the value on the way in, so
   `tracking_state == "normal"` is a safe test in the viewer. The layer records this in its caveats.

4. **`claim_level` values are lowercase.** `ObservationMeasurement.claimLevel` is a Swift
   `String` enum whose raw values are `descriptive`, `qualified`, `measured` (not `DESCRIPTIVE` /
   `QUALIFIED` / `MEASURED`). Measurements are copied verbatim, so those are the strings in
   `measurements.json`. A missing value means `descriptive`.

5. **`measurements[].value` may be `null`.** A record that carries an `unsupported_reason` records
   an attempt, not a result. The viewer prints the reason in place of a value, and a tag report
   never computes a delta from such a record.

6. **`observations[].measurement_ids` is derived, not copied.** The export's `Observation` has no
   such field; the builder joins `measurements.jsonl` to observations through
   `measurements[].sourceFrameIDs` against `observations[].evidence[].frameID`. Likewise
   `contact_hazard` is folded from `evidence[].sceneDescription.contactHazardProbability / Taxon /
   ModelIdentifier`, which is where the export actually keeps it.

7. **`twin.json.builder` gains `build_key`.** The SHA-256 of the sorted source hashes, the builder
   version and the options that change the output. It is how `build_twin.py` decides that a rebuild
   would produce the same package and does nothing. Readers may ignore it.

8. **`visit.json` carries `layers` and `caveats`.** `layers` is the list of layer ids in that visit
   (the same information the manifest holds, in visit order); `caveats` is where a visit says
   something true about all of it at once, such as "the observations in this visit are synthetic".

9. **`transforms.json` records also carry `schema_version: 1` at the document level**, matching
   `twin.json`.

10. **A registered fit must keep at least 8 inliers and at least half its matches.** `rmse_m` on a
    RANSAC fit is an *inlier* RMSE, so three lucky cameras out of thirty would otherwise report a
    tiny residual and pass the 3 % gate. This is builder policy rather than file format, but it is
    recorded here because it is the difference between a registration and a coincidence; a fit that
    fails it is written `unregistered` with the counts it actually achieved.

## Schema notes (viewer)

Defects and clarifications found while implementing `twin-viewer/`. Nothing above is renamed.

1. **`twin.json.integrity` is a build-time snapshot, not a live invariant.** The viewer appends to
   `audit.jsonl` (and to `anchors.jsonl` / `tags.jsonl`) through the local server and never rewrites
   the manifest, so the moment anybody tags anything, `integrity.audit_event_count` and
   `integrity.audit_head_hash` fall behind the journal. `twinlib.schema.validate_package` currently
   reports that as a failure, which makes a package invalid the first time it is used. The correct
   test — the one `serve.py --check` applies — is that the journal has only grown: the recorded head
   hash must still be the hash at seq `audit_event_count - 1`, and the journal must be no shorter
   than the recorded count. Growth beyond that is reported as a note. A shorter journal, or a
   recorded head that is not at the recorded position, is a real failure. The builder should either
   adopt the same rule or rename the block so it reads as a snapshot (`built_with` rather than
   `integrity`).

2. **`stations[].timestamp`, `captured_at` and the intrinsics are optional in practice.** In
   `fixtures/curb-02` all 163 stations carry a `camera_to_world_column_major` and nothing else: no
   timestamp, no `fx/fy/cx/cy`, no `width/height`, no `tracking_state`, no `image`. The viewer
   therefore scrubs the timeline in capture order and says so rather than inventing a clock, and it
   draws the photo plane as a fallback rectangle labelled "shows direction only" rather than
   inventing a calibration. The stations section should state that only `id` and
   `camera_to_world_column_major` are required.

3. **There is no `tag.updated` action.** Renaming a tag or giving it a taxon is a new revision in
   `tags.jsonl` (last revision per id wins), and the viewer records it as `note.added` with the new
   revision in the payload, because that is the only allowlisted action that fits. If tag editing is
   meant to be a first-class operation the action list needs `tag.updated`.

4. **`POST /events` validates before the server-assigned fields exist.** `twinlib.schema.validate_record("event", …)`
   requires `id`, `seq`, `at`, `prev_hash` and `hash`, all of which the server assigns. `serve.py`
   fills them in (with a provisional hash) before validating, then lets `append_event` recompute
   `seq`, `prev_hash` and `hash` under the file lock. Worth stating in the server-contract section so
   another implementation does not validate the caller's half-event and reject every write.

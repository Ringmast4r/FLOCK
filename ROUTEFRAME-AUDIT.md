# Independent RouteFrame Audit

Prepared July 29, 2026 for the FLOCK project maintainer and future development agents.

This is a constructive, read-only review of commit `9387a188d7996f8c5fdadcc765bbc9074774406b`. The goal is to identify what is already valuable, what needs stronger evidence or engineering controls, and how this project could become a more trustworthy surveillance-transparency resource.

No live-site behavior or existing project file was changed as part of the audit.

## Executive conclusion

FLOCK is a compelling public-awareness prototype with a clear visual idea: combine camera records with agency-sharing relationships and make the scale understandable on a map.

The current repository should not yet be treated as an authoritative camera or agency-sharing database. Several implementation choices can silently merge records, convert agency-level relationships into camera-level claims, expose the page to untrusted HTML, and obscure source provenance.

The most valuable feature is the network-sharing visualization. It should be rebuilt around reviewed agency-level evidence rather than attached to individual camera points by coordinate.

## Audit scope

The review covered:

- `README.md`
- `DATA_SOURCES.md`
- `DEPLOY.md`
- `index.html`
- `create_tiles.py`
- `merge_osm_global.py`
- `data/tiles/index.json`
- `camera_networks.json`
- A representative California tile, `data/tiles/6/10/24.json`
- Repository contents, commit history, GitHub Pages deployment, and live response headers

The review did not establish the correctness of every one of the 336,708 records. It is not legal advice and does not determine whether every upstream source is licensed for every downstream use.

## What the project does well

### 1. The public-interest purpose is clear

The README explicitly frames the project as privacy education, journalism, research, and public awareness. It also rejects vandalism, harassment, illegal activity, and evasion.

### 2. The map is approachable

The legend, device filters, clustering, camera popups, and network lines turn a difficult subject into something a general audience can explore.

### 3. The published top-level totals reconcile

The tile index contains 512 tiles and reports 336,708 records. Summing the tile counts also produces 336,708.

The standalone `camera_networks.json` file contains 4,253 network objects and 113,829 relationship entries, matching the headline connection total.

### 4. Spatial tiling is the right general direction

Dividing a large dataset geographically is better than forcing every visitor to download and render the full database at startup.

## Priority findings

### High: Agency relationships are presented as camera-level facts

The application attaches an agency's full partner list to individual camera points. When a relationship endpoint does not match a loaded camera, the application creates a green marker, labels it as a police station, and says that it receives data from the selected camera network.

The underlying partner data includes organizations such as:

- Vendor and integration companies
- Demo organizations
- Training organizations
- Test organizations
- Commercial customers
- Agencies whose physical endpoint has not been established

An agency-level access relationship does not prove that:

- Every camera operated by that agency shares with every listed partner
- A particular camera was active during the reported period
- The destination coordinate is a police station
- A destination organization continuously receives data
- The sharing relationship is current

#### Recommended correction

Model sharing as its own evidence object:

```json
{
  "relationshipId": "stable-source-derived-id",
  "sourceUrl": "https://...",
  "sourcePublisher": "official portal or reviewed publisher",
  "retrievedAt": "2026-07-29T00:00:00Z",
  "effectiveFrom": null,
  "effectiveTo": null,
  "sourceAgency": {
    "name": "Example Police Department",
    "jurisdiction": "Example, State"
  },
  "destinationAgency": {
    "name": "Example County Sheriff",
    "jurisdiction": "Example County, State"
  },
  "relationshipType": "portal access",
  "scope": "unknown",
  "reviewStatus": "reviewed",
  "limitations": [
    "Does not establish camera-level participation",
    "Does not establish current access"
  ]
}
```

Render these relationships in a separate agency-sharing view. Do not connect the relationship to a camera unless the source specifically identifies that camera.

If a location is only an agency headquarters, city centroid, or geocoding result, label it as approximate. Do not label an inferred point as a police station.

### High: Untrusted data is inserted directly into HTML

The page builds HTML strings from:

- Operator names
- Manufacturer and brand fields
- Agency partner names
- Network names
- Portal URLs
- Nominatim search results

These values are inserted with `innerHTML`, Leaflet popup HTML, and inline `onclick` attributes without HTML escaping or URL validation.

Community map records and remote API responses must be treated as untrusted. A malicious or malformed upstream string could alter the popup or execute script in a visitor's browser.

#### Recommended correction

- Construct DOM elements and assign untrusted values through `textContent`.
- Do not generate inline event handlers.
- Validate external links with `new URL`.
- Permit only `https:` destinations.
- Add `rel="noopener noreferrer"` to new-window links.
- Add a restrictive Content Security Policy.
- Self-host or integrity-pin Leaflet and marker-cluster assets.
- Add tests containing HTML-like operator, manufacturer, partner, and search-result values.

Do not publish an exploit example in project documentation or tests served by GitHub Pages.

### High: Four-decimal coordinate keys silently merge records

The ingestion, tile generation, network lookup, and browser marker store use coordinates rounded to four decimal places as record identity.

That is not a stable camera identifier. It can collapse separate cameras on nearby poles, opposite sides of a road, adjacent intersections, or dense facilities. It can also discard source differences and contradictory metadata.

In the representative California tile:

- Source features: 5,957
- Unique four-decimal marker keys: 5,107
- Features sharing an already-used marker key: 850
- Network objects: 718
- Unique four-decimal network keys: 670
- Network key collisions: 48

The standalone network file also contains 83 repeated four-decimal source keys.

#### Recommended correction

- Preserve the upstream source type and stable source ID.
- For OpenStreetMap, retain the element type and OSM ID.
- Use a namespaced key such as `osm:node:123456`.
- Keep multiple records at the same or nearby coordinates.
- Deduplicate only through an explicit reconciliation process.
- Record which source fields were merged and which conflicts remain.
- Never discard a later source merely because its rounded coordinate matches an earlier record.

### High: The published data pipeline is not reproducible from this repository

`DATA_SOURCES.md` says the EFF, Private Eyes, OpenStreetMap, geocoding, deduplication, confidence scoring, and multi-format export pipeline are implemented.

The documented files `download_multi_source.py`, `create_enhanced_map.py`, integration reports, and raw-source workspace are not present in the repository.

Without the transformation code and receipts, another agent cannot determine:

- Which exact source versions were used
- How agency records became point coordinates
- How camera and agency records were distinguished
- How relationships were generated
- Which records were removed as duplicates
- Which source won when values conflicted
- Whether the public database can be reproduced

In the inspected California tile, 1,157 of 5,957 records contained a `source` or `source:url` field. A source string such as `survey`, `GPS`, or `local knowledge` is useful context, but it is not always a retrievable evidence link.

#### Recommended correction

Publish a deterministic builder that produces:

- A source manifest with URLs, retrieval times, hashes, and license notes
- Raw-source receipts or documented acquisition instructions
- A normalized intermediate schema
- A reconciliation report
- A rejected-record report
- A source-coverage report
- The final tiles

Every public record should retain its stable upstream identifier and original source link when available.

### Medium: Privacy and provider controls need disclosure and enforcement

The search form invites city, place, and address searches. Submitted text goes directly from the visitor's browser to the public Nominatim service.

The current implementation has no application-wide request coordination, shared rate limit, cache, provider-status reporting, or privacy page.

The My Location function keeps coordinates in browser state, which is good. However, moving the map to the precise position causes third-party base-map tile requests around that location. Visitors should understand which providers receive requests and that those providers control their own logs.

The public Nominatim service requires application-wide traffic to remain under its limits and recommends proxying, caching, and the ability to switch providers.

#### Recommended correction

- Put geocoding behind a same-origin service.
- Enforce one application-wide upstream request per second or the current provider requirement.
- Cache normalized searches using hashed cache keys.
- Search only after an explicit user action.
- Add timeouts, cancellation, and a human-readable unavailable state.
- Disclose provider processing and retention boundaries.
- Avoid intentional application logging of raw address text, route text, or precise user coordinates.

### Medium: Licensing needs a concrete repository-level decision

The README says `MIT License (or your choice)`, but there is no `LICENSE` file. That phrase is not a clear code license grant.

The database combines OpenStreetMap-derived records with other sources. The repository needs to distinguish:

- Code license
- OpenStreetMap-derived database obligations
- Other source licenses or public-record status
- Map-tile terms
- Attribution requirements
- Any records whose reuse rights remain unclear

#### Recommended correction

- Add a real `LICENSE` file for the code.
- Add `DATA-LICENSES.md`.
- Document the license or reuse basis for each source.
- State whether the merged database is offered under ODbL, treated as a collective database, or structured another way after legal review.
- Put legible OpenStreetMap attribution and a license link next to the live map.

### Medium: The tile loader is not memory-bounded

The map loads tiles on demand, but it never evicts them. Every loaded feature, network object, marker, and cluster remains in memory for the rest of the session.

The published 512 tiles total approximately 115.6 MB. The largest individual tile is approximately 8.8 MB, and 16 tiles exceed 2 MB.

The `Show ALL Lines` action draws only relationships from tiles already loaded into the session. It does not load and render all 113,829 global relationships, although the wording implies that it does.

#### Recommended correction

- Rename the action to `Show loaded relationships`, or deliberately load a documented bounded scope.
- Track visible and recently used tiles.
- Evict off-screen records and layers.
- Abort stale requests when the viewport changes.
- Consider vector tiles or a MapLibre GeoJSON/vector-tile source.
- Separate global summary counts from currently loaded counts.
- Expose loading, partial, unavailable, stale, and complete states.

## RouteFrame comparison

RouteFrame and FLOCK overlap, but they serve different primary purposes.

| Area | FLOCK today | RouteFrame principle |
| --- | --- | --- |
| Primary experience | Global surveillance map and network display | United States route transparency, education, and reviewed research |
| Camera evidence | Mixed global records with uneven provenance | Public records remain distinct from reviewed evidence |
| Missing data | Often implied through map presence or absence | Missing remains unknown and never becomes zero or camera-free |
| Operator and vendor | Can show Flock Safety as operator or manufacturer depending on the source | Operator and vendor are separate fields and ownership is not inferred |
| Sharing relationships | Attached visually to camera points | Should be reviewed agency-level evidence |
| Place search | Browser directly calls public Nominatim | Same-origin processing, caching, request controls, and disclosure |
| Route analysis | Not present | Compares ordinary lawful routes against incomplete public ALPR records |
| Freshness | Static November 2025 snapshot | Rolling source status with timestamps and partial or stale states |

The larger FLOCK camera total is not directly comparable to an ALPR inventory. It mixes ALPR, general video surveillance, gunshot detectors, and other records across global geography.

Useful public RouteFrame references:

- https://routeframe.io/methodology
- https://routeframe.io/data-limitations
- https://routeframe.io/privacy
- https://routeframe.io/alpr-camera-map
- https://routeframe.io/intelligence

## Recommended development order

### Phase 1: Prevent misleading or unsafe output

1. Replace untrusted HTML interpolation with safe DOM construction.
2. Validate every external URL.
3. Stop labeling unknown endpoints as police stations.
4. Rename `Show ALL Lines`.
5. Add visible data freshness and limitations.

### Phase 2: Restore stable identity and provenance

1. Preserve upstream source IDs.
2. Remove four-decimal coordinates as record identity.
3. Publish the complete transformation pipeline.
4. Produce source-coverage and collision reports.
5. Separate camera, agency, jurisdiction, and relationship entities.

### Phase 3: Build a reviewed agency-sharing product

1. Normalize official portal and Private Eyes relationships.
2. Preserve source links, retrieval dates, and effective periods.
3. Review relationship type and scope.
4. Display unknown and expired states.
5. Add list and table views alongside network graphics.

### Phase 4: Harden operations

1. Add automated schema and regression tests.
2. Add a build and validation workflow before Pages deployment.
3. Add privacy-safe geocoding controls.
4. Add CSP and dependency integrity controls.
5. Test desktop, 390-pixel, and 320-pixel layouts.
6. Test large and sparse tiles under throttled networking.

## Minimum automated checks

Future agents should be able to run one documented command that checks:

- Valid GeoJSON and network schemas
- Stable unique record IDs
- Source URL coverage
- Duplicate and near-duplicate reports
- Operator and manufacturer separation
- Relationship-source coverage
- Coordinate validity
- Safe rendering of HTML-like source strings
- HTTPS-only publisher and portal links
- Tile totals against the source manifest
- Current README counts against generated data
- No unsupported camera-level sharing claims

## Questions for the maintainer

1. Can the missing multi-source integration scripts and source manifests be published?
2. What exact Private Eyes fields produced `camera_networks.json`?
3. Are relationship endpoints agency headquarters, municipal centroids, geocoding results, or verified facilities?
4. Should demo, vendor, commercial, and training organizations be excluded from the police-agency graph?
5. What license should apply to the code?
6. What license and reuse basis should apply to each database layer?
7. Is the intended product a global camera map, a Flock-specific accountability tool, or a broader agency-sharing research system?

## Final assessment

The project has a strong idea and a useful public-interest direction. Its relationship graph could become genuinely important if it is rebuilt with stable identities, source-level evidence, honest uncertainty, safe rendering, and a reproducible pipeline.

Until those corrections are made, this repository is best described as an exploratory visualization based on mixed public and community records. It should not be described as proof that a particular camera shares data with a particular agency, that every green endpoint is a police station, or that the database is complete or current.

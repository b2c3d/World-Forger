### Unity Spline Integration

When Routing is set to **Custom**, the Village Forger uses Unity's Spline package
        to define road paths. This provides complete artistic control over road layout.

### How It Works

The engine samples each assigned spline at high-precision intervals (0.5m) to trace
            the curve through the grid. Each sample point is converted to grid coordinates by dividing
            by Resolution, and the corresponding grid cells are marked as road cells.

### Custom Spline Assignment

In the VillageForgerConfig inspector (Roads → Generation tab), you can add multiple
            `SplineContainer` references. Each container can hold multiple splines, and you
            can select specific spline indices or use all splines in the container. The inspector
            enforces mutual exclusion — the same spline index cannot be assigned to both
            Main and Side roads.

!!! tip
    **Tip:** You can use multiple splines in one container. The Village Forger will
            merge them all into a single, complex road network. The inspector shows spline indices with
            color-coded Scene view overlays (cyan for main, magenta for side).

### Obstacle Avoidance

The engine uses **batch rasterization** to detect and avoid existing scene geometry
        before placing buildings.

### Configuration

**`Precise Obstacle Detection`** · `bool`

When enabled, performs pixel-perfect obstacle detection by checking actual mesh triangles and physics volumes at every grid cell. Significantly more accurate for complex shapes (rivers, curves), but more CPU-intensive on large grids. When disabled, uses bounding-box approximation only.

*Default: true*

---

**`Obstacle Check Height`** · `float`

The vertical height (in meters) above the terrain to sweep for obstacles. Increase this value to catch overhead obstacles like bridges or tree canopies. Decrease to ignore high-altitude objects that won't interfere with building placement. Example: 5.0 catches most buildings and structures, 20.0 catches tall bridges.

*Default: 5.0*

---

**`Show Obstacle Gizmos`** · `bool`

When enabled, displays detailed debug information in the Scene view showing which grid cells are blocked by obstacles. Shows grid coordinates and the name of the blocking object. Useful for diagnosing unexpected building placement failures.

*Default: false*

---

### Detection Pipeline

**`Step 0: Boundary Spline (optional)`**

If a **Boundary Spline** is assigned on the
                `VillageForgerConfig`, the engine first rasterizes it via scanline polygon fill.
                All cells outside the spline are marked as obstacles and excluded from every subsequent
                step — typically eliminating 30–80% of the grid before any physics query runs.

---

**`Step 1: Mesh Pre-Cache`**

`FindObjectsByType<MeshRenderer>` is called
                **exactly once** per run. Renderers that have any `Collider`
                in their parent or child hierarchy are skipped — colliders are already caught by the
                raycast pass in Step 2. For non-collider renderers (typical for water planes, decals,
                stylized terrain decorations), vertices are pre-transformed to world space and triangles
                are bucketed into a CSR grid aligned with the village cell grid. This makes the per-cell
                point-in-mesh test O(k) instead of O(T).

---

**`Step 2: Precise — Batched Raycasts`**

When **Precise Obstacle Detection** is enabled, one
                downward ray per active cell is assembled into a `NativeArray<RaycastCommand>`
                and dispatched with `RaycastCommand.ScheduleBatch`. All rays execute in parallel
                across worker threads via the Unity Jobs system. Cells already marked by the boundary pass
                are excluded from the batch, so raycast count is proportional to the *active* cell count,
                not the full grid.

---

**`Step 2 (alt): Fast — OverlapBox`**

When Precise is disabled, a single `Physics.OverlapBox`
                call retrieves every collider inside the grid volume, and each collider's AABB is rasterized
                directly into cell coordinates. Much cheaper, but misses curves and complex shapes.

---

**`Step 3: Mesh Triangle Lookup`**

For cells that the raycast did not hit, the pre-built triangle buckets
                from Step 1 are queried. Only the triangles overlapping that specific cell's XZ footprint
                are tested for point-in-triangle — no full mesh scan.

---

**`Step 4: Height Filter`**

Every ray hit and mesh-triangle hit is compared against the cached
                terrain height at that cell (pre-populated by `VillageTerrainCache`). Hits at or
                below the ground are discarded, so underground rocks and submerged geometry do not block
                placement.

---

**`Step 5: Cell Marking`**

Surviving hits mark cells as both *occupied* and *obstacle*.
                Buildings, roads, and overlays will not be placed into those cells.

---

!!! warning
    **Performance Note:** Obstacle detection runs once at generation time, not per-frame.
            On a 160×160 grid with a closed Boundary Spline and Precise Obstacle Detection enabled,
            typical generation cost is well under 50 ms — scanline fill, compacted parallel raycasts,
            and triangle bucketing combine to keep the hot path roughly O(W·H + S·H + rays/cores + k·W·H)
            instead of the quadratic-per-cell cost of a naive implementation. All physics queries finish
            before placement begins; there is zero runtime cost after generation.

### Output Tracking (ForgerOutput)

The `ForgerOutput` component is an internal marker system that ensures robust
        tracking of all procedurally generated objects.

### Why Markers?

Tracking by component rather than by name ensures that generated objects can always
be found and cleaned up, regardless of how they are renamed or reorganised in the
Hierarchy. The marker system decouples identification from naming entirely.

### How It Works

**`Tagging`**

All procedurally generated objects (Holders, Splines, Overlays) are tagged
                with a `ForgerOutput` component upon creation.

---

**`Detection`**

The editor uses `ForgerOutput` markers to locate all generated objects reliably,
independent of their names in the Hierarchy.

---

**`Auto-Demolish`**

`Build()` automatically calls `Demolish()` before
                starting a new generation, preventing procedural objects from stacking.

---

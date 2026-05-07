# Village Forger Profile

The Profile is a ScriptableObject containing the shared "DNA" of a village — road rules,
        building definitions, debug colors, and diagnostics. Multiple Village Forger instances can share
        the same profile, while each instance maintains its own grid dimensions and spline assignments
        via the `VillageForgerConfig` component.

The profile editor is organized into four main tabs: **Layout**, **Roads**,
        **Buildings**, and **System**, each with their own sub-tabs.

### Layout → Grid

!!! info
    **Instance vs Profile:** Width, Height, Grid Offset, and the Boundary Spline are stored on the
            `VillageForgerConfig` instance component, not the shared profile. Resolution is on the profile.

**`Width`** · `int`

Grid width in cell units. Controls the east-west extent of the village.
            Also adjustable via Scene view corner handles.

---

**`Height`** · `int`

Grid height in cell units. Controls the north-south extent of the village.

---

**`Grid Offset`** · `Vector2`

Shifts the grid relative to the GameObject pivot. Useful for centering the village
            on a specific terrain feature without moving the root object.

---

**`Boundary Spline`** · `SplineContainer`

Optional **closed** spline that defines a custom-shaped village footprint.
            Every grid cell whose center falls *outside* the spline is automatically marked as an obstacle
            and skipped by the rest of the detection pipeline — so you get both custom silhouettes (circle,
            irregular coastline, estate boundary, etc.) and a large performance win, because expensive collider
            and mesh checks are only done for cells inside the boundary.

The spline is rasterized using a **scanline polygon fill**
            (O(W·H + S·H) instead of O(W·H·S)), so even fine boundaries with
            hundreds of samples add only a few milliseconds to each run. If the assigned spline is not closed,
            boundary detection is skipped and a warning is logged both in the Inspector and in the Console.

*Default: null (no boundary; entire grid is considered)*

---

**`Resolution`** · `float`

World-space size of each grid cell in meters. Controls the scale of
            the entire village layout. Lower values produce finer detail; higher values produce coarser
            layouts. Think of it as pixel size: small Resolution = high detail, large Resolution = coarse layout.
            Usually 1 for stylized art, 2–4 for realistic.

*Default: 1.0  |  Min: 0.1*

---

### Layout → Village Square

**`Enable Village Square`** · `bool`

When enabled, places a central plaza at the midpoint of the main road.
            The village square acts as a focal point for the settlement layout.

*Default: true*

---

**`Square Size (Cells)`** · `int`

The footprint of the village square in grid cells (width and height).
            Larger values create a grander central plaza.

*Default: 3  |  Min: 1*

---

**`Square Spacing (Cells)`** · `int`

Clear buffer of cells surrounding the village square that blocks house placement.
            Creates breathing room around the plaza.

*Default: 1  |  Min: 0*

---

**`Snap To Terrain`** · `bool`

Snap the village square stamp to the terrain height at its placement location.
            Disable if your village square prefab handles its own vertical positioning.

*Default: true*

---

**`Village Square Stamp`** · `string`

The stamp name emitted for the village square area. Must exactly match a
            Stamp Rule's `StampName` in one of the assigned Stencils.

*Default: VillageSquare*

---

### Layout → Ground Fill

Controls how empty grid cells (those not occupied by roads, village square, or buildings) are
        filled with ground stamps when generating.

**`Ground Stamp`** · `string`

The stamp name emitted for empty ground fill cells. Must exactly match a
            Stamp Rule's `StampName` in one of the assigned Stencils. One ground stamp is emitted per grid cell marked as empty.
            Each stamp is positioned at the cell’s world-space center.

*Default: VillageGround*

---

**`Snap To Terrain`** · `bool`

Snap ground fill stamps to the terrain height. Disable if your ground
            prefabs handle their own vertical positioning (e.g. they use their own raycasting or are
            placed at a fixed Y level).

*Default: true*

---

**`Skip Ground In Buffer`** · `bool`

When enabled, ground stamps are skipped in cells reserved as building
            spacing buffers. Reduces visual clutter at building edges where ground tiles would clip
            through foundations.

*Default: false*

---

### Layout → Obstacles

**`Obstacle Layers`** · `LayerMask`

The Forger avoids placing buildings on top of existing scene objects on these
            layers (e.g. Environment, Water). Uses dual detection: `Physics.OverlapBox` for
            colliders plus `MeshRenderer` bounds for non-collider meshes like water planes.
            Only objects whose top surface is above the terrain height are treated as obstacles.

*Default: None (no obstacle avoidance)*

---

### Roads → Main Roads

### Routing

**`Routing`** · `MainRoadRouting`

Determines how the main road is routed through the grid.

---

### Road Width

**`Thickness`** · `int`

Half-width of the main road in grid cells. 0 produces a single-cell-wide road;
            1 produces a 3-cell-wide road (1 center + 1 on each side).

*Default: 0  |  Min: 0*

---

### Curves

**`Segments Min`** · `int`

Minimum number of bezier control points for the main road.
            More segments produce more organic curvature.

*Default: 2  |  Min: 1*

---

**`Segments Max`** · `int`

Maximum number of bezier control points. The actual count is chosen randomly
            within the Min/Max range.

*Default: 6  |  Min: 1*

---

**`Amplitude Min`** · `float`

Minimum lateral deviation of curve control points from the straight centerline,
            in grid cells. 0 produces a perfectly straight road.

*Default: 2.0  |  Min: 0*

---

**`Amplitude Max`** · `float`

Maximum lateral deviation of curve control points, in grid cells.
            Higher values produce more winding roads.

*Default: 8.0  |  Min: 0*

---

### Spline Export

**`Auto Export Splines`** · `bool`

When enabled, procedurally generated roads are automatically exported to a child
            `SplineContainer` at generation time. The splines conform to terrain height and can be
            used by other systems (e.g. Spline Mesh, traffic AI).

*Default: false*

---

**`Spline Resolution`** · `float`

How frequently (in Unity units) a spline knot is placed to conform to the terrain.
            Lower values produce more knots and a tighter terrain fit, but increase spline complexity.

*Default: 5.0  |  Min: 0.5*

---

**`Height Offset`** · `float`

Vertical lift applied to the generated splines to prevent Z-fighting with the
            terrain surface.

*Default: 0.1*

---

### Stamp

**`Main Road Stamp`** · `string`

The stamp name emitted for main road cells. One stamp is emitted per grid cell
            that the road passes through. Must exactly match a Stamp Rule's `StampName` in one of the assigned Stencils.

*Default: VillageMainRoad*

---

### Microverse Splines (optional)

When the [Microverse Splines](https://assetstore.unity.com/packages/tools/terrain/microverse-splines-232974)
        package is installed, the Village Forger can attach a `JBooth.MicroVerseCore.SplinePath` component
        to every generated main-road spline. The SplinePath component carves the terrain heightmap, paints splat
        layers, and clears trees and details along the spline at runtime. These settings are only visible in the
        inspector when the package is installed; otherwise the section is hidden.

**Build-order note:** Microverse only carves terrain when the SplinePath component sits under
        a `MicroVerse` scene root. Move the Village Forger GameObject under your MicroVerse hierarchy
        (or vice versa) for the integration to actually affect terrain.

**`Use Microverse Spline`** · `bool`

Master toggle. When enabled, every generated main-road spline GameObject
            (`MainRoad_NN`) gets a `SplinePath` component configured from the settings below.
            When disabled, no SplinePath is attached and the rest of this section is hidden in the inspector.

*Default: false*

---

### Microverse → Common

**`Width`** · `float`

Spline carving width in world units — how wide the heightmap modification is.

*Default: 4.0*

---

**`Smoothness`** · `float`

Falloff distance at the spline edges. Higher values produce a softer transition
            into the surrounding terrain.

*Default: 2.0*

---

**`Trench`** · `float`

Vertical depth of the carved trench in world units. Positive values push the
            terrain down (typical for roads); negative values raise it (e.g. embankments).

*Default: 0.2*

---

**`Modify Height Map`** · `bool`

When enabled, the spline modifies the terrain heightmap.
            Disable to leave the height untouched and only paint splats / clear vegetation.

*Default: true*

---

**`Modify Splat Map`** · `bool`

When enabled, the spline applies splat (terrain texture) layers along its path.

*Default: true*

---

**`Splat Weight`** · `float`

Blend strength of the splat layer.

*Default: 1.0  |  Range: 0 – 1*

---

**`Splat Width`** · `float`

Width of the splat application along the spline.
            Often set wider than `Width` to feather the texture beyond the trench edges.

*Default: 4.0*

---

**`Layer`** · `TerrainLayer`

Primary terrain texture layer painted along the spline (e.g. dirt road, cobblestone).

---

**`Embankment Layer`** · `TerrainLayer`

Secondary terrain texture layer painted at the spline edges where the trench
            fades back to surrounding terrain (e.g. roadside grass, gravel shoulder).

---

**`Clear Trees`** · `bool`

When enabled, terrain trees within the clearing radius are removed along the spline.

*Default: true*

---

**`Tree Width`** · `float`

Tree-clearing radius along the spline.

*Default: 4.0*

---

**`Clear Details`** · `bool`

When enabled, terrain detail objects (grass, rocks, etc.) are removed along the spline.

*Default: true*

---

**`Detail Width`** · `float`

Detail-clearing radius along the spline.

*Default: 4.0*

---

**`Treat as Spline Area`** · `bool`

When enabled, the spline is treated as a closed area (e.g. a village square)
            rather than a linear path. Only meaningful for closed splines.

*Default: false*

---

### Microverse → Advanced

**`Blend`** · `float`

Overall blend factor of the height-map modification. 0 = no effect on the
            existing terrain; 1 = full replacement. Useful for previewing the carve at reduced strength.

*Default: 1.0  |  Range: 0 – 1*

---

**`Use Trench Curve / Trench Curve`** · `bool + AnimationCurve`

When enabled, the trench depth is modulated by the curve across the spline width
            (x = 0 at the centre, x = 1 at the edge). Default is an ease-in-out from full depth at the centre to
            zero at the edges.

---

**`Use Texture Curve / Texture Curve`** · `bool + AnimationCurve`

When enabled, the splat weight is modulated by the curve across the spline width.

---

**`Use Tree Curve / Tree Curve`** · `bool + AnimationCurve`

When enabled, the tree-clearing strength is modulated by the curve across the spline width.

---

**`Use Detail Curve / Detail Curve`** · `bool + AnimationCurve`

When enabled, the detail-clearing strength is modulated by the curve across the spline width.

---

**Noise blocks.** Each of the four noise channels below shares the same set of fields,
        documented once. By default `Type` is `None` — in that state the rest of
        the noise fields are collapsed and the channel contributes nothing.

**`Position Noise`** · `Noise`

Adds organic deviation to the spline path itself.

---

**`Width Noise`** · `Noise`

Varies the carving width along the spline.

---

**`Height Noise`** · `Noise`

Varies the trench depth along the spline.

---

**`Splat Noise`** · `Noise`

Varies the splat-layer application strength along the spline.

---

**Noise fields (per channel):**

**`Type`** · `enum`

Type of noise. `None` disables this channel; otherwise pick from
            `Simple`, `FBM`, `Worley`, `Worm`, `WormFBM`,
            or `Texture`.

*Default: None*

---

**`Space`** · `enum`

`World` samples in world space (consistent across the level);
            `Stamp` samples relative to the spline.

*Default: World*

---

**`Frequency`** · `float`

Spatial frequency of the noise. Higher values produce smaller features.

*Default: 10.0*

---

**`Amplitude`** · `float`

Multiplier on the noise output. Higher values produce stronger displacement / variation.

*Default: 1.0*

---

**`Offset`** · `float`

Constant added to the noise output before amplitude.

*Default: 0.0*

---

**`Balance`** · `float`

Skews the noise toward higher (positive) or lower (negative) values.

*Default: 0.0  |  Range: -0.5 – 0.5*

---

### Microverse → Quality

**`SDF Resolution`** · `enum`

Resolution of the internal Signed Distance Field used for the spline.
            Higher values produce more accurate carving at the cost of memory and processing time.
            Options: `K256`, `K512`, `K1024`, `K2048`.

*Default: K512*

---

**`Search Quality`** · `enum`

Quality of the closest-point-on-spline search. Higher quality produces more
            accurate results but increases update time. Options: `VeryLow`, `Low`,
            `Medium`, `High`, `VeryHigh`, `ExtremelyHigh`.

*Default: Medium*

---

### Roads → Side Roads

### Routing

**`Routing`** · `SideRoadRouting`

How side roads are generated.

---

### Count

**`Count Min`** · `int`

Minimum number of procedural side roads generated per run.
            Ignored when Count Fixed is greater than 0.

*Default: 2  |  Min: 0*

---

**`Count Max`** · `int`

Maximum number of procedural side roads. The actual count is chosen randomly
            within the Min/Max range.

*Default: 6  |  Min: 0*

---

**`Count Fixed`** · `int`

If greater than 0, always generates exactly this many side roads, overriding
            Min/Max. Set to 0 to use the Min/Max range instead.

*Default: 0*

---

### Length & Spacing

**`Length Fraction`** · `float`

Side road length as a fraction of the longest grid axis. 0 produces very
            short roads; 0.5 means they can extend half the grid length.

*Default: 0.5  |  Range: 0 – 0.5*

---

**`Min Pivot Spacing`** · `int`

Minimum cell spacing between side road attachment points on the main road.
            Prevents roads from spawning too close together.

*Default: 6  |  Min: 0*

---

**`Stop When Hit Road`** · `bool`

If enabled, a side road stops extending when it meets an existing road cell.
            Prevents road overlap and creates a cleaner, more logical street network.

*Default: true*

---

### Road Width

**`Thickness`** · `int`

Half-width of side roads in grid cells. Works the same way as main road thickness.

*Default: 0  |  Min: 0*

---

### Curves

**`Segments Min`** · `int`

Minimum number of curve segments for side roads.

*Default: 1  |  Min: 1*

---

**`Segments Max`** · `int`

Maximum number of curve segments for side roads.

*Default: 4  |  Min: 1*

---

**`Amplitude Min`** · `float`

Minimum lateral curve amplitude for side roads, in grid cells.

*Default: 1.0  |  Min: 0*

---

**`Amplitude Max`** · `float`

Maximum lateral curve amplitude for side roads, in grid cells.

*Default: 6.0  |  Min: 0*

---

**`Angle Jitter`** · `float`

Random angular variation applied to each side road's starting direction, in degrees.
            0 means always perpendicular to the main road; higher values create more organic layouts.

*Default: 25°  |  Range: 0 – 90*

---

### Spline Export

**`Auto Export Splines`** · `bool`

When enabled, procedurally generated roads are automatically exported to a child
            `SplineContainer` at generation time. The splines conform to terrain height and can be
            used by other systems (e.g. Spline Mesh, traffic AI).

*Default: false*

---

**`Spline Resolution`** · `float`

How frequently (in Unity units) a spline knot is placed to conform to the terrain.
            Lower values produce more knots and a tighter terrain fit, but increase spline complexity.

*Default: 5.0  |  Min: 0.5*

---

**`Height Offset`** · `float`

Vertical lift applied to the generated splines to prevent Z-fighting with the
            terrain surface.

*Default: 0.1*

---

### Stamp

**`Side Road Stamp`** · `string`

The stamp name emitted for side road cells. Must exactly match a
            Stamp Rule's `StampName` in one of the assigned Stencils.

*Default: VillageSideRoad*

---

### Microverse Splines (optional)

Side Roads expose the same Microverse Splines integration as Main Roads. When the
        [Microverse Splines](https://assetstore.unity.com/packages/tools/terrain/microverse-splines-232974)
        package is installed and **Use Microverse Spline** is enabled, every generated side-road
        spline GameObject (`SideRoad_NN`) gets a `SplinePath` component configured from
        these settings — independent of the main road's settings, so side roads can use a different width,
        terrain layer, or noise profile.

See Roads → Main Roads → Microverse Splines above for the full
        property reference. The Side Road settings are identical in structure and behaviour, just applied to
        side-road splines instead of main-road splines.

### Buildings → Residential

**`House Spacing (Cells)`** · `int`

This value controls the **scan step** (also called the stride) that the placement
                algorithm uses when walking across the grid looking for valid house locations. It does
                *not* add a gap or buffer between buildings — it determines **how many grid
                cells the algorithm skips between each candidate position it checks**.

**How it works:** The Forger scans the grid from corner to corner in a nested loop,
                advancing by `step` cells in both X and Y. At each sampled position it tries to fit
                one of your enabled house types — checking that the footprint is clear and that at least
                one edge touches a road. A lower step means more positions are checked and more houses are placed;
                a higher step means fewer positions are checked and placement becomes sparse.

**Example on a 20×20 grid:**

**Why high values fail:** Each candidate position must satisfy two conditions:
                the full footprint must be clear of roads, buildings, and obstacles, *and* at least one
                edge must be adjacent to a road cell. With only a handful of candidate positions, most will
                be blocked by roads, the village square, special buildings, or obstacle geometry — leaving
                nowhere valid for houses.

**When set to 0 (auto):** The algorithm automatically uses the smallest dimension
                among all enabled house types as the step. For example, if your smallest house is 2×2, the
                step becomes 2. This is the recommended default — it produces a well-populated village
                without checking unnecessarily many positions.

**Recommendation:** Leave this at **0** unless you specifically want
                a sparser village. Values of 1–3 are safe. Values above 4 should only be used on very
                large grids (100+ cells per axis). The inspector will display a warning if the value is high
                enough to cause placement issues on your current grid size.

*Default: 0 (auto)  |  Min: 0*

---

### House Definition Properties

Each entry in the House Types list defines a residential building type.

**`Enabled`** · `bool`

Toggle this house type on or off without removing it from the list.

---

**`Building Name`** · `string`

The name used for the Stamp and in the Inspector (e.g. "Peasant Hovel").
                Must exactly match a Stamp Rule's `StampName` in one of the assigned Stencils.

---

**`Snap To Terrain`** · `bool`

When enabled, the building's Y position is set to the terrain height at its
                placement location using high-precision raycasting.

*Default: true*

---

**`Rotate To Face Road`** · `bool`

Automatically rotates the building to face the nearest road using a weighted
                tangent calculation. Creates natural-looking street-facing architecture.

*Default: true*

---

**`Size`** · `Vector2Int`

The footprint in grid cells. **X = Frontage** (road-facing edge),
                **Y = Depth** (perpendicular to road). Ensure your prefabs fit within these dimensions
                multiplied by Resolution.

*Default: (2, 2)*

---

### Buildings → Specialized

Special buildings are landmark structures with priority-based placement and flexible road requirements.

### Special Building Definition Properties

**`Enabled`** · `bool`

Toggle this special building on or off.

---

**`Building Name`** · `string`

The exact stamp name (e.g. "VillageManor"). Must match a
                Stamp Rule's `StampName` in one of the assigned Stencils.

---

**`Snap To Terrain`** · `bool`

Snap this building to the terrain height at its placement location.

*Default: true*

---

**`Rotate To Face Road`** · `bool`

Rotate the building to face the nearest road.

*Default: true*

---

**`Size`** · `Vector2Int`

The footprint of this building in grid cells (width, depth).

*Default: (3, 3)*

---

**`Priority`** · `int`

Higher priority buildings are placed first. Use this to ensure important landmarks
                (church, manor) get prime road-adjacent slots before less important structures.

*Default: 10*

---

**`Placement`** · `SpecialPlacementRule`

Controls which roads this building can be placed alongside.

*Default: Flexible*

---

**`Skip Fallback`** · `bool`

When enabled, the Forger will not try side roads if main road placement fails.
                The building is simply omitted from the layout. Only relevant when Placement is set to Flexible.

*Default: false*

---

### System → Debug Colors

These colors control the terrain-conforming debug overlay mesh. Each cell type gets a distinct color
        for easy identification.

**`Main Road Color`** · `Color`

Overlay color for main road cells.

*Default: Red*

---

**`Side Road Color`** · `Color`

Overlay color for side road cells.

*Default: Yellow*

---

**`Empty Color`** · `Color`

Overlay color for empty ground cells.

*Default: Blue*

---

**`Village Square Color`** · `Color`

Overlay color for the village square area.

*Default: Orange*

---

**`Special Building Color`** · `Color`

Overlay color for special building footprints.

*Default: Purple*

---

**`House Color`** · `Color`

Overlay color for residential house footprints.

*Default: Green*

---

**`Obstacle Color`** · `Color`

Overlay color for cells blocked by scene geometry obstacles. Only visible when **Show Obstacle Gizmos** is enabled.

*Default: Red*

---

**`Overlay Offset`** · `float`

Vertical lift applied to the overlay mesh to prevent Z-fighting with the
            terrain surface.

*Default: 0.05*

---

### System → Overlay Shader Properties

Control the appearance of the procedural grid overlay visualization. The overlay uses a dual-layer system:
        **major grid lines** mark cell boundaries, and **minor grid lines** show internal world-unit subdivisions.

**`Global Alpha`** · `float`

Overall transparency of the entire overlay mesh (0 = invisible, 1 = fully opaque).

*Default: 0.5*

---

**`Major Grid Color`** · `Color`

Color and alpha of the major grid lines that mark cell boundaries (grid-cell resolution).

*Default: Black with 0.7 alpha*

---

**`Major Thickness`** · `float`

Thickness of major grid lines in world units. Range: 0.005 to 0.2.

*Default: 0.05*

---

**`Minor Grid Color`** · `Color`

Color and alpha of the minor grid lines that subdivide each cell (showing the CellSize world-unit divisions).

*Default: Black with 0.3 alpha*

---

**`Minor Thickness`** · `float`

Thickness of minor grid lines in world units. Range: 0.005 to 0.1.

*Default: 0.02*

---

!!! info
    **Height snapping — heightmap first, raycast as fallback.**
            Each overlay vertex is lifted to terrain height before drawing. The visualizer prefers
            the injected `IVillageTerrainCache.GetHeight` heightmap read — it sees only
            terrain, never building meshes — so the overlay stays flat under buildings instead of
            climbing over their roofs. If no terrain cache is available, it falls back to a downward
            physics raycast restricted to the active terrain's layer (never the Default layer where
            spawned buildings live), then to the raw vertex height plus `YOffset`. This
            ordering was a deliberate fix — earlier builds raycast first against the Default mask
            and produced "tents" wherever buildings sat under the overlay.

### System → Diagnostics

**`Log Placement Warnings`** · `bool`

Logs a warning to the Console when a special building cannot be placed anywhere
            on the grid. Helpful for identifying when your grid is too small or too crowded for all
            defined buildings.

*Default: true*

---

**`Strict Placement`** · `bool`

When enabled, generation aborts entirely if any special building cannot be placed.
            Useful for strict layout validation during development.

*Default: false*

---

**`Verbose Diagnostics`** · `bool`

Logs detailed per-building placement pass/fail results to the Console.
            Use this to diagnose why specific buildings are not appearing in the layout.

*Default: false*

---

### System → Object Naming

These control the names of procedurally generated GameObjects in the hierarchy. The
        `ForgerOutput` marker system tracks these objects by component, not name, so renaming
        is safe.

**`Output Holder Name`** · `string`

The name of the root GameObject that holds all generated village objects.

*Default: __WorldForgerOutput__*

---

**`Road Splines Name`** · `string`

The name of the GameObject holding the exported road splines.

*Default: __WorldForgerRoadSplines__*

---

**`Debug Overlay Name`** · `string`

The name of the GameObject holding the debug overlay mesh.

*Default: __WorldForgerOverlay__*

---

### Village Forger — Frequently Asked Questions
FAQ 1
### Q: I set House Spacing to 5 (or higher) and now no houses appear. Why?

**House Spacing** is not a gap or buffer between buildings — it is the
            **scan step** (stride) the placement algorithm uses when walking across your grid
            looking for valid house locations. The algorithm starts at one corner of the grid and advances
            by this many cells in both X and Y at each step. At every position it lands on, it checks
            whether a house footprint fits there (clear of roads, obstacles, and other buildings) and
            whether at least one edge touches a road.

A high step value means the algorithm **skips over most of the grid** and only
            checks a handful of positions. On a 20×20 grid with a step of 5, only about 16 positions
            are checked. After subtracting positions blocked by roads, the village square, special buildings,
            and obstacles, there may be zero valid spots left — so no houses get placed.

!!! tip
    **Fix:** Set House Spacing to **0** (auto). The algorithm will
                automatically use the smallest enabled house dimension as the step, which produces a
                well-populated village without unnecessary scanning overhead.

FAQ 2
### Q: Why does House Spacing = 1 produce more houses than House Spacing = 0 (auto)?

When set to **0 (auto)**, the algorithm does not use a step of 1. Instead, it
            calculates the step from the smallest dimension of your enabled house types. For example, if
            your smallest house is 2×2, the auto step becomes **2**. This means:

| Setting | Actual Step | Positions on 20×20 Grid |
| --- | --- | --- |
| 0 (auto) | 2 (smallest house dim) | ~100 |
| 1 | 1 (every cell) | ~400 |

A step of 1 checks **every single cell**, so it can find valid placements that a
            step of 2 skips over. For example, a valid 2×2 slot at position (1, 1) would be missed
            when stepping by 2 (which checks 0, 2, 4…) but caught when stepping by 1.

In practice, the difference is usually small. Auto (step = 2) already produces a
            well-populated village while avoiding redundant overlap checks. Setting the step to 1 is more
            thorough but does roughly 4× more work — rarely necessary unless you need every
            possible slot filled on a tight grid.

!!! tip
    **Recommendation:** Leave at **0 (auto)** for most use cases. Only
                set to 1 if you notice gaps in placement and want maximum coverage.

FAQ 3
### Q: My special building says "placement failed" in the console. What can I do?

Special buildings are placed **before** residential houses, in descending
            **Priority** order. Each one needs a contiguous block of empty cells matching its
            Size, with at least one edge adjacent to a road. Placement can fail for several reasons:
- The grid is too small for the building’s footprint plus the surrounding road and spacing requirements.
- The building’s **Placement** rule restricts it to main-road-only or side-road-only cells, and there aren’t enough qualifying positions.
- Higher-priority buildings already consumed the best positions.
- Obstacles (scene objects on your Obstacle Layers) are blocking candidate areas.

!!! tip
    **Troubleshooting steps:**
    
    Enable **Verbose Placement Diagnostics** (System → Diagnostics) to see exactly which positions were tried and why each failed.
    Try changing the building’s **Placement** rule to `Flexible` so it can use both main and side roads.
    Reduce the building’s **Size** if it’s too large for your grid.
    Increase your grid dimensions to give more room.
    Lower the **Priority** so other buildings don’t claim the best spots first.

FAQ 4
### Q: What is the difference between the Village Profile and the Village Config?

The **Village Forger Profile** is a `ScriptableObject` asset that defines
            *what* a village looks like — road shapes, building types, curve parameters, stamp
            names, debug colors, and all the shared rules. It can be reused across multiple village instances
            for visual consistency.

The **Village Forger Config** is a `MonoBehaviour` component on a
            specific GameObject in your scene. It holds *instance-specific* data: the grid Width and
            Height, the Grid Offset, custom spline assignments, and a reference to which Profile to use.
            Two villages in the same scene can share the same Profile but have different grid sizes and positions.

!!! info
    **Think of it this way:** The Profile is the blueprint (shared DNA), and the Config
                is the building site (unique location and dimensions).

FAQ 5
### Q: Why do buildings overlap or float above the terrain?

**Overlapping:** Buildings are placed on a grid, so overlap typically means two
            building types have footprint sizes that don’t tile cleanly with the scan step, or the
            **Cell Size** doesn’t match your art assets. Make sure each building prefab
            fits within its defined **Size** (in cells) multiplied by the profile’s
            **Cell Size**. For example, a 2×2 house on a Cell Size of 3 occupies a
            6×6 unit area.

**Floating:** Ensure **Snap to Terrain** is enabled on the house or
            special building definition. The Forger uses high-precision raycasting to sample the terrain
            height at each placement position. If Snap to Terrain is off, the building spawns at the
            grid’s Y origin, which may not match the terrain surface.

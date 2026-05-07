![World Forger](images/WorldForgerBanner.png)

# Getting Started

World Forger is a decoupled procedural generation engine for Unity. It separates layout logic from visual theming,
        allowing level designers and technical artists to work independently. Layouts emit abstract **Stamps**
        which are resolved into prefabs by **Stencils** (node-graph assets).

### Requirements

World Forger requires **Unity 6.4** or later and the following packages. All are available
        via the Unity Package Manager.

**`Unity 6.4+`** · `Editor`

Minimum Unity version. Required for the Experimental GraphView API used by the Stencil Graph editor and current URP compatibility.

---

**`GraphView (built-in)`** · `UnityEditor.Experimental.GraphView`

The Stencil Graph editor is built directly on Unity's bundled
            `UnityEditor.Experimental.GraphView` namespace. No external package install is
            required — it ships with the editor.

---

**`Mathematics`** · `com.unity.mathematics 1.3.3`

High-performance math library used internally for grid calculations, spatial hashing,
            and deterministic random number generation.

---

**`Splines`** · `com.unity.splines 2.8.2`

Unity's native spline system. Used by the Village Forger for custom road paths and
            auto-exported procedural splines that follow terrain.

---

!!! info
    **No third-party graph package needed.** Earlier builds of World Forger relied on
            Unity's experimental `com.unity.graphtoolkit` package and a `.forgetheme`
            ScriptedImporter. The current build uses GraphView directly and stores everything inside a
            single `WorldForgerGraphAsset` — no import step, no sidecar backup file, no
            experimental package install.

### Folder Structure

!!! note
    **Note on Moving Files:** You may rename or move the root `WorldForger` folder to any location within your project (e.g., `Assets/b2c3d`). However, you **must not** change the internal folder structure (Editor, Runtime, Documentation, etc.) as the toolkit relies on these relative paths to locate assets and documentation.

### Core Concepts

<div class="grid cards" markdown>

-   **The Stamp**

    An abstract placeholder in 3D space with a **Name**, **Position**,
            **Rotation**, and **Scale**. It represents the *intent* to place an
            object, not the object itself.

-   **The Forger**

    Any component that generates stamps. The **Village Forger** is a complex macro-forger
            that creates entire settlements. The **Prefab Forger** is a micro-forger for
            individual themed objects.

-   **Stencil Graph**

    A node-based `WorldForgerGraphAsset` that maps stamp names to prefabs. When the
            engine encounters a stamp named "House", the Stencil decides which house prefab to spawn.
            The same asset opens in the Stencil Graph editor and drops directly into a Forger's
            **Stencils** slot — no bake step.

-   **Spatial Salting**

    A per-location randomization algorithm that ensures every placement makes independent random choices.
            This prevents repetitive "all or nothing" patterns across the generated layout.

</div>

### The Pipeline

Every generation run follows the same four-stage pipeline:

<div class="grid cards" markdown>

-   **1. Demolish**

    All previously generated objects are destroyed. The `ForgerOutput` marker system
            ensures nothing is left behind, even if object names were changed.

-   **2. Build Layout**

    The Forger runs its spatial algorithm (grid placement, road generation, building scanning) and
            stores the result as internal data structures.

-   **3. Emit Stamps**

    The layout is converted into a flat list of named stamps at world-space positions. Each stamp
            carries a name, transform, and optional metadata.

-   **4. Stencil Apply**

    The `WorldForgerEngine` resolves each stamp against the assigned Stencils,
            spawns the chosen prefabs, and parents them under the output holder.

</div>

### Resolution — The Master Scale

**Resolution** controls how many Unity meters each grid cell represents. Think of the
    village grid like an image: Resolution is the pixel size.

<div class="grid cards" markdown>

-   **Small Resolution (e.g. 1)**

    High detail. More cells per meter. Finer building placement and road curves.
            Best for stylized or small-scale art where 1 Unity unit = 1 meter.

-   **Large Resolution (e.g. 4)**

    Coarse layout. Fewer cells, faster computation. Best for realistic art where buildings
            occupy several meters. A 2×2 house becomes 8m × 8m in world space.

</div>

### How Resolution Affects the System

**`World Positioning`**

The generator operates in abstract grid coordinates. Resolution translates these to meters.
                A house at grid position (10, 15) with Resolution 4 appears at world coordinates (40m, 60m).

---

**`Custom Splines`**

When using custom Unity Splines, the engine measures the spline's physical world length
                and divides by Resolution to rasterize the smooth curve into grid cells.

---

**`Obstacle Avoidance`**

Obstacle bounding boxes are divided by Resolution to determine how many grid cells
                each obstacle blocks.

---

**`Scene Handles`**

The physical footprint of your village is always
                `Width × Resolution` by `Height × Resolution`.
                Handle movements snap to `1 / Resolution` increments.

---

!!! tip
    **Art Style Scaling:** If you swap from realistic assets (1 unit = 1 meter) to stylized
            (1 unit = 5 meters), just change Resolution to 5. Your building definitions (e.g. "2×2 house")
            stay the same — you adapt the entire village to a new art scale by changing one number.

![](../images/VillageForgerBanner.png)

# Village Forger

The Village Forger is a high-level layout engine that creates organic, grid-based settlements.
        It generates road networks, places buildings alongside roads, and supports terrain conforming,
        obstacle avoidance, and custom spline-driven roads.

### Stencils

**`Stencils`** · `StencilAsset[]`

One or more Stencils that map stamp names to prefabs. Stencils are
            searched in array order when generating — the first Stencil whose Stamp Rule matches
            the emitted stamp wins. Stack multiple Stencils to layer overrides (a "Halloween" Stencil
            in front of the year-round one) or to mix biomes.

---

### Generate Settings

**`Randomize Seed`** · `bool`

When enabled, picks a new random seed every time `Build()` is called.
            The Seed field is ignored when this is active.

---

**`Seed`** · `int`

The random seed used for layout generation and prefab selection. Changing this
            value completely changes the village layout. Set to `0` to pick a new random seed
            each run. Disabled in the inspector when Randomize Seed is checked.

---

**`Auto Generate On Start`** · `bool`

Automatically calls `Build()` when the scene enters Play mode.
            Disable this if you want to trigger generation manually at runtime.

*Default: true*

---

**`Show Debug Visualization`** · `bool`

Toggles a terrain-conforming mesh overlay that visualizes the village blueprint.
            Color-coded by cell type (road, house, village square, etc.). Useful for seeing the layout without
            spawning heavy 3D assets.

*Default: true*

---

**`Auto Generate On Move`** · `bool`

When enabled, dragging the yellow grid handles or moving the GameObject in the
            Scene view will instantly trigger a re-generation. Provides a live-preview workflow.

*Default: false*

---

### Actions

These buttons appear at the bottom of the Village Forger inspector.

**`Generate`**

Runs the full generation pipeline: Demolish → Build Layout →
            Emit Stamps → Stencil Apply. Supports full undo and shows a progress bar during execution.

---

**`Randomize`**

Sets the Seed to a new random value between 1 and `int.MaxValue`.
            If Auto Generate On Move is active, also triggers an immediate re-generation.

---

**`Demolish`**

Destroys all procedurally generated objects (buildings, roads, overlays, splines).
            Shows a confirmation dialog before proceeding. Enabled whenever any child with a
            `ForgerOutput` marker is detected.

---

**`Bake GameObject`**

Moves all generated children out of the Forger hierarchy into a new standalone
            GameObject. This "bakes" the procedural output into a permanent scene object that no longer
            depends on the Forger. Live-preview tracker components
            (`ForgerStampInstance` and `ForgerChildStampInstance`) are
            stripped from the baked hierarchy — once detached from the Forger they serve no
            purpose. Fully undoable.

---

!!! tip
    **Single-step undo.** Generate and Demolish are each collapsed into a single undo
            group — one ++ctrl+z++ reverts an entire generation (spawned prefabs, holder,
            overlay mesh, and road splines) in one step. The debug overlay mesh persists across re-generations
            and only swaps its mesh data, so successive runs don’t add spurious undo entries.
            Undo is editor-only; in Play mode these actions are immediate.

### Scene View Handles

When a Village Forger is selected, the Scene view displays interactive handles for grid manipulation.

**`Grid Outline`**

A white rectangle showing the current grid boundaries in world space,
            respecting the GameObject's position, rotation, and scale.

---

**`Corner Handles`**

Yellow sphere handles at the bottom-left and top-right corners. Drag to resize
            the grid and shift its offset simultaneously. Movements snap to Resolution increments for
            precise alignment.

---

**`Spline Overlays`**

When using Custom routing, spline knots are highlighted with sphere caps and
            index labels. Main road splines appear in **cyan**,
            side road splines in **magenta**.

---


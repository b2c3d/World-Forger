![](../images/PrefabForgerBanner.png)

# Prefab Forger

The Prefab Forger is a precision tool for placing individual procedurally-themed items.
        It emits a single stamp at its transform position and resolves it through the assigned
        Stencils. Useful for props, hero assets, and any object that needs themed variation
        without a full layout system.

### Stencils

**`Stencils`** · `StencilAsset[]`

One or more Stencils (typically `WorldForgerGraphAsset`)
            that map stamp names to prefabs. Stencils are searched in array order — the first
            with a matching Stamp Rule wins. Displayed as a reorderable list in the inspector.

---

!!! info
    **Project Diagnostics:** The inspector header shows how many Stencil assets
            exist in your project. If zero are found, create one via
            **Assets → Create → World Forger → Stencil**.

### Stamp

**`Stamp Name`** · `string`

The stamp name emitted at this GameObject's world transform. Must
            match a Stamp Rule's `StampName` in one of the assigned Stencils. When
            Stencils are assigned, this field becomes a dropdown populated with every Stamp Rule
            name discovered across the array. If the current value doesn't match any rule, it
            shows with a "(missing)" suffix.

*Default: "Prefab"*

---

### Generate Settings

**`Randomize Seed`** · `bool`

Generates a cryptographically strong random seed before every run, ignoring
            the Seed field. Ensures high-quality variation for hero assets and unique placements.

*Default: true*

---

**`Seed`** · `int`

Manual seed for deterministic output. Disabled when Randomize Seed is checked.
            Set to 0 for a random seed each run.

*Default: 0*

---

**`Auto Generate On Start`** · `bool`

Automatically calls `Build()` when the scene enters Play mode.

*Default: true*

---

### Actions

**`Generate`**

Runs the full pipeline: Demolish → Emit Stamp → Stencil Apply.
            Supports undo and shows a progress bar.

---

**`Randomize`**

Generates a new cryptographically strong seed, disables Randomize Seed
            (to lock the seed), and immediately triggers a run.

---

**`Destroy`**

Removes all procedural output. Enabled whenever any child with a
            `ForgerOutput` marker is detected.

---

**`Bake GameObject`**

Moves the generated children into a new standalone GameObject named after the
            Stamp Name. The baked object no longer depends on the Forger. Live-preview tracker
            components (`ForgerStampInstance` and `ForgerChildStampInstance`)
            are stripped from the baked hierarchy — once detached from the Forger they serve
            no purpose. Fully undoable.

---


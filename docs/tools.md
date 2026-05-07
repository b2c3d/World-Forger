### Village Profile Browser

A dockable editor window that lists every `VillageForgerProfile` asset in the project,
        shows each one's key stats at a glance, and offers one-click actions to apply, duplicate, rename,
        ping, or delete them. Treat it as the "Project window for Village Profiles."

!!! info
    **Open it three ways:**
    
    Menu: `World Forger → Village Forger → Village Profile Browser`
    Menu: `Window → World Forger → Village Forger → Village Profile Browser`
    Button: **Browse Profiles** on any Village Forger Config inspector (next to **Create New**)

### Card Grid

The centre of the window shows every profile in the project as a styled card. The grid
            automatically reflows its column count to match the window width. Each card displays:
- Profile name (bold)
- Cell Size
- Main Road Routing and Side Road Routing
- Count of *enabled* house types and special buildings
- Whether the central village square is on or off
- **Apply** button (green) — assigns this profile to every selected Village Forger in the scene
- **Select** button — focuses the details panel on this profile (clicking anywhere on the card does the same)

### Details Panel

The right-hand panel shows deeper information for the selected profile:
- **Asset** — name and asset path
- **Summary** — cell size, routing modes, side road count range, road thicknesses, market square size, enabled-vs-total house and special counts, precise obstacle toggle
- **Validation warnings** — live output of `VillageForgerProfile.Validate()` (e.g. "No House Types are enabled")
- **Rename** — edit the asset name inline and click *Apply Rename*

### Actions

**`Apply to Selected Forger`**

Assigns the selected profile to every `VillageForgerConfig`
                currently selected in the scene. Changes are registered with `Undo.RecordObjects`,
                so Ctrl+Z reverts the assignment. Button label reflects the count when multiple Forgers are selected.

---

**`Duplicate`**

Creates a copy of the profile next to the original using
                `AssetDatabase.CopyAsset`. The new asset gets an auto-numbered name
                (e.g. `MyProfile 1.asset`) and is auto-selected for immediate renaming.

---

**`Ping in Project`**

Highlights the asset in the Project window so you can see where it lives on disk.

---

**`Open in Inspector`**

Sets the profile as Unity's active selection so the Inspector tab shows its full editor
                — useful for fine-tuning colours, curve ranges, and other fields not summarised on the card.

---

**`Delete`**

Permanently deletes the profile asset after a confirmation dialog.
                Any Village Forger Configs that referenced it will have their Profile field cleared.
                **Not undoable via Ctrl+Z** — restore from version control if needed.

---

### Toolbar
- **Search** — filters the grid by profile name (case-insensitive substring match)
- **Result count** — shows "filtered / total" so you always know how many profiles exist
- **Refresh** — forces a re-scan of the project (happens automatically on any asset change)
- **New Profile** — opens a *Save File* dialog so you choose the exact location for the new asset; the created profile is initialized with `ResetToDefaults()`, auto-selected in the browser, and pinged in the Project window

!!! info
    **Resizable details panel.** The vertical bar between the card grid and the details
            panel is a drag handle — hover it for the resize cursor, drag to move. The width persists in
            EditorPrefs so your preferred layout survives Unity restarts.

!!! info
    **Play Mode behaviour:** The window stays open and functional across play/edit transitions.
            Applying a profile during Play mode is allowed and undo-tracked, but remember that scene changes made
            in Play mode are reverted on exit.

### Stencil Graph Browser

A dockable editor window that lists every `WorldForgerGraphAsset` (stencil) in the
        project, surfaces each one's wiring and validation state at a glance, and offers one-click
        actions to open in the graph editor, apply to selected Forger(s), duplicate, rename, ping, or
        delete. Mirrors the Village Profile Browser's dual-pane layout but works against stencils —
        which apply to *any* Forger type, not just Village.

!!! info
    **Open it two ways:**
    
    Menu: `World Forger → Stencil Graph Browser`
    Menu: `Window → World Forger → Stencil Graph Browser`

### Card Grid

The centre of the window shows every stencil in the project as a styled card. The grid
            reflows its column count to match the window width. Each card displays:
- Stencil name (bold)
- Stamp Rule count — "*X* wired / *Y* total"
- Total prefab cards (single Prefab nodes plus Prefab Array nodes)
- Validation glyph — `✓ no warnings` or `⚠ N warnings`,
            from `StencilGraphBuilder.Validate()`
- **Open** button (green) — opens this stencil in the Forger Graph editor
- **Select** button — focuses the details panel on this stencil
            (clicking anywhere on the card does the same)

### Details Panel

The right-hand panel shows deeper information for the selected stencil:
- **Asset** — name and asset path
- **Summary** — counts for stamp rules wired-vs-total, prefab nodes,
            prefab arrays, stamp emitters, and edges
- **Stamp Rules** — one row per Stamp Rule in the graph showing
            "*StampName* → *N* prefabs" or "*StampName* → (no wiring)".
            Lets you spot empty stamps at audit time
- **Validation** — full output of
            `StencilGraphBuilder.Validate()`, displayed as warning helpboxes
- **Rename** — edit the asset name inline and click *Apply Rename*

### Apply to Selected Forger

Unlike Village Profiles (which slot into a single field on a Forger Config), a Forger's
            `Stencils` is a *list*. The browser surfaces both common workflows:

**`Set as only Stencil`**

Replaces every selected Forger's `Stencils` array with a
                single-element array containing the picked stencil. Use this when the picked stencil is
                meant to be the sole authoritative source.

---

**`Add to Stencils`**

Appends the picked stencil to every selected Forger's existing
                `Stencils` list. No-op for Forgers that already reference this stencil, so
                re-clicking is safe. Use this when stacking stencils for layered overrides
                (e.g. a "Halloween" stencil on top of a base village).

---

Both modes record an Undo step so Ctrl+Z reverts the change. Multi-Forger selection is
            handled in both modes — the button label reflects the count when multiple Forgers are selected.

### Actions

**`Open in Graph Editor`**

Routes through `WorldForgerGraphWindow.Open` — focuses
                an existing window if one is already showing this stencil, otherwise opens a new graph
                window with the stencil loaded.

---

**`Duplicate`**

Creates a copy of the stencil next to the original via
                `AssetDatabase.CopyAsset`. The new asset gets an auto-numbered name and is
                auto-selected for immediate renaming.

---

**`Ping in Project / Open in Inspector`**

Standard navigation shortcuts — Ping highlights the asset in the
                Project window; Open in Inspector sets it as Unity's active selection.

---

**`Delete`**

Permanently deletes the stencil asset after a confirmation dialog.
                Forgers referencing the deleted stencil will have it removed from their Stencils list
                automatically by Unity. **Not undoable via Ctrl+Z** — restore from
                version control if needed.

---

### Toolbar
- **Search** — filters the grid by stencil name (case-insensitive substring match)
- **Result count** — shows "filtered / total" so you always know how many stencils exist
- **Refresh** — forces a re-scan of the project (also happens automatically on any asset change)
- **New Stencil** — forwards to `World Forger → Create → Forger Graph`,
            which creates a fresh stencil in the active Project-window folder and opens it in the graph editor

!!! info
    **Resizable details panel.** The vertical bar between the card grid and the details
            panel is a drag handle — hover it for the resize cursor, drag to move. The width persists in
            EditorPrefs so your preferred layout survives Unity restarts.

### Variant Generator

A dockable editor window that generates a batch of seed variants for any Forger, captures a
        top-down thumbnail of each, and lets you pick the one you like best to apply to the live scene.
        Think of it as a “contact sheet” for procedural layouts — roll a dozen seeds at
        once, compare them side-by-side, and commit the winner with one click.

!!! info
    **Open it two ways:**
    
    Menu: `World Forger → Variant Generator`
    Button: **Generate Variants** at the bottom of the Actions section on any
                *Village Forger* or *Prefab Forger* inspector (disabled in Play mode)

### Toolbar Fields

**`Target Forger`** · `Forger`

The Forger the batch will run against. Drag any Village Forger or
                Prefab Forger GameObject into the slot. If the window is opened with nothing assigned,
                it auto-picks from the current Selection.

---

**`Variant Count`** · `int slider (1 – 32)`

How many variants to generate in the batch. The card grid reflows to
                fit; larger counts take proportionally longer.

---

**`Base Seed`** · `int`

**0** means every variant gets a fresh random seed —
                a non-deterministic batch that’s different every time you press Generate.
                **Non-zero** means the batch is deterministic: the same Base Seed always
                produces the same sequence of variants, so you can reproduce a previous batch exactly.

*Default: 0 (random batch)*

---

**`Thumbnail Size`** · `popup — 256 / 512 / 1024 px`

Resolution of the captured thumbnails. Higher resolutions produce
                sharper cards but consume more VRAM. The details-panel preview and the whole panel width
                also scale with this setting, so picking a larger size gives you a bigger on-screen preview.

*Default: 512*

---

**`Generate/Regenerate`**

Kicks off the batch. Shows a cancelable progress bar while each
                variant is generated and captured. The label changes to **Regenerate** once
                a batch is already loaded.

---

### Card Grid

After generation, each variant is shown as a card in a reflowing grid on the left. Every card
            displays:
- Top-down thumbnail of the generated layout
- **Variant N** label
- Seed used for the variant
- Time (ms) taken to generate
- **Select** button — focuses the details panel on this variant (clicking
            anywhere on the card does the same)
- **Apply** button — applies this variant’s seed to the target Forger
            immediately, without having to open the details panel first

### Details Panel

The right-hand panel shows a larger view of whichever variant is currently selected. Its width
            and the preview size both scale with the chosen Thumbnail Size.
- **Large preview** — the variant’s thumbnail at full panel size
- **Prev / `Variant 3 / 12` / Next** — cycle through the batch
            without having to click cards
- **Seed** — the seed value that produced this variant
- **Generate Time** — milliseconds for this variant’s run
- **Holder Count** — number of output holders spawned by the Forger
- **Apply to Scene** — writes the selected variant’s seed to the
            target Forger and triggers a full re-generation in the scene
- **Copy Seed to Clipboard** — handy for pasting into the Forger’s
            Seed field manually, or sharing with collaborators

### Undo & Safety

**`Batch undo group`**

The entire variant batch collapses into a single undo group named
                *“Generate N Forger Variants”*. One ++ctrl+z++ reverts the whole
                batch — you will never end up with a half-undone pile of scratch objects in the scene.

---

**`Apply to Scene undo`**

Applying a variant is its own independent undo step, separate from
                the batch. Ctrl+Z reverts the seed change and scene re-generation without touching the
                captured thumbnails.

---

**`Cancel-safe`**

Pressing **Cancel** in the progress bar stops the batch
                after the current variant finishes. Whatever has already been generated is kept, so you
                can start picking from a partial batch immediately.

---

**`Error resilience`**

If an individual variant’s `Build()` throws, the
                error is logged to the Console and the batch continues with the next seed. One bad
                variant cannot kill the whole run.

---

!!! info
    **Thumbnails are editor-session-only.** Captured thumbnails live in memory and are
            discarded when the window closes. *Nothing is written to disk.* If you want to keep a
            particular layout, apply it to the scene (which bakes the seed into the Forger) or copy its seed
            to the clipboard before closing the window.

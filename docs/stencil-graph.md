# Stencil Graph

The Stencil Graph is a non-linear interpreter that converts abstract stamp data into physical
        game objects. It is built on Unity’s built-in `UnityEditor.Experimental.GraphView`
        API, providing a fully visual node-based editor for defining how stamps map to prefabs.
        **Stencils** (`WorldForgerGraphAsset`) are the core creative asset of
        the system — the very same asset you edit in the graph window is the runtime asset a
        Forger consumes at generation time. There is no import step, no sidecar backup file, no
        compile pass.

### Graph Editor

The Stencil Graph editor is a custom GraphView window that opens when you double-click a
        `WorldForgerGraphAsset` in the Project window. It provides a full node-graph
        canvas with drag-and-drop prefab assignment, color-coded node types, integrated live
        preview, and inline validation.

### Editor Features

**`Node Canvas`**

Standard GraphView canvas with pan, zoom, box selection, and
                copy/paste. Right-click the canvas background to open the node creation menu
                (Add Stamp Rule, Add Prefab, Add Sticky Note).

---

**`Color-Coded Nodes`**

Each node type has a distinct header stripe for quick visual identification:
                **Green** = Stamp Rule,
                **Blue** = Prefab.
                Edges connect a Stamp Rule's *output* port to a Prefab's *input* port,
                building the candidate list for that rule.

---

**`Auto-Save`**

The editor flushes to disk on focus loss (clicking another window)
                and on close, so edits land on the asset without an explicit save action — just
                like an Inspector field. ++ctrl+s++ still saves the current scene as usual.

---

**`Persistent View State`**

Pan offset, zoom scale, and each node's *collapsed* state are
                serialised onto the asset (`ViewOffset`, `ViewScale`,
                `StampRuleNodeData.Collapsed`, `PrefabNodeData.Collapsed`) so
                you return to the same view across sessions and domain reloads.

---

!!! tip
    **Tip — evaluation order:** Prefab Nodes are evaluated in the order their
            edges were connected to the Stamp Rule. Reorder by removing and re-adding an edge if you
            want a particular candidate to roll first. `StopFlow` on a Prefab terminates the
            roll early once it spawns — useful for prioritising rare variants.

### Inspecting Nodes

Clicking any node on the canvas selects it and immediately populates Unity’s Inspector
        panel with a dedicated editor for that node type — no need to navigate nested foldouts
        or open a separate properties window.

### What Each Inspector Shows

**`Stamp Rule`**

Enabled toggle, Stamp Name, and Position / Rotation / Scale
                offsets applied to every candidate that spawns under this rule.

---

**`Prefab Node`**

Prefab reference (drag-and-drop), Weight, behavioral flags
                (Stop Flow, Static Mode, Externally Managed, Nav Static), Position / Rotation /
                Scale offsets, Spawn Filters, and the per-node Preview Settings override.

---

**`Prefab Array Node`**

Prefabs list, Weight, the same behavioral flags as Prefab Node,
                Position / Rotation / Scale offsets, and Spawn Filters. All members of the array
                share the same probability and flags.

---

**`Stamp Emitter Node`**

Stamp Name (the child stamp to fire after the parent prefab
                spawns) and Position / Rotation / Scale offsets relative to the spawned parent.

---

!!! tip
    **Tip — Live Preview & Undo:** Inspector edits trigger Live Preview
            exactly like inline edits. Transform drags use the fast re-pose path (no respawn); structure
            changes — prefab swap, name rename, flag toggle — trigger a full scene rebuild.
            All Inspector edits are recorded in Unity’s Undo stack; ++ctrl+z++ works as
            expected.

### Toolbar Reference

The toolbar runs along the top of the Stencil Graph window. Buttons are arranged left to
        right in roughly the order you reach for them during a typical editing session.

**`Live`** · `toggle`

Live Preview mode. **ON by default** for every newly opened graph
            window — every transform/random/probability edit you make in the graph debounces for
            300 ms and is applied to the active scene's Forger automatically. The button is amber when
            active. Click to pause (useful before bulk restructuring on a large scene where the slow-path
            `Forger.Build()` would stall the editor). See
            Live Preview for the fast-path
            vs. slow-path semantics.

---

**`Apply`** · `button`

Force-flushes any pending Live Preview change immediately rather than
            waiting for the 300 ms debounce window. Useful when you want to drag a slider, then
            instantly see the result without releasing the mouse.

---

**`Fit`** · `button`

Frames all nodes to fit the current window. Shortcut: ++f++
            with the canvas focused frames the current selection if any nodes are selected, otherwise
            frames the whole graph.

---

**`Tidy`** · `button`

Auto-layout pass. Stamp Rule nodes are stacked in a left column and
            their connected Prefab nodes are arranged in tidy rows to the right, sorted by edge order.
            Sticky notes and orphan prefabs are not moved. Undoable with ++ctrl+z++.

---

**`Map`** · `toggle`

Shows or hides the floating MiniMap in the bottom-right corner. The
            MiniMap is draggable and shows your current viewport rectangle — useful for large
            graphs where Tidy alone isn't enough to keep your bearings.

---

**`Search`** · `text field`

Filters nodes by stamp name, prefab name, or sticky-note title.
            Matches are highlighted; non-matching nodes are dimmed. Press ++ctrl+f++ to focus
            the field, ++esc++ to clear it. The first match auto-frames in the canvas.

---

### Keyboard Shortcuts

All shortcuts are active while the Stencil Graph window has focus.

**`F`**

Frame the current selection. With nothing selected, frames the
            entire graph (same as the toolbar's **Fit** button).

---

**`Delete`**

Remove the selected nodes, edges, or sticky notes. Deleting a node
            also removes any edges attached to it. Operation is undoable.

---

**`Ctrl+D`**

Duplicate selection in place — cloned nodes retain settings but
            get fresh GUIDs and an offset position so they don't sit on top of the originals. Edges
            between duplicated nodes are also recreated.

---

**`Ctrl+C / Ctrl+X / Ctrl+V`**

Copy / cut / paste. Paste targets the current mouse position so you
            can move the selection between regions of the graph or even between two open Stencil
            Graph windows.

---

**`Ctrl+F`**

Focus the toolbar Search field. ++esc++ from the field clears
            the filter and returns focus to the canvas.

---

**`Mouse wheel / Alt+Drag`**

Standard GraphView pan and zoom. Middle-mouse drag also pans.

---

### Creating Stencils

To create a new Stencil:

**`Step 1`**

Create a `WorldForgerGraphAsset` via the Project window:
            **Create → World Forger → Stencil**. Name the new asset (e.g.
            `VillageStencil`).

---

**`Step 2`**

Double-click the asset (or use **Window → World Forger
            → Forger Graph** and load it) to open the Stencil Graph editor. You will see
            an empty canvas with a toolbar across the top.

---

**`Step 3`**

Right-click the canvas and choose **Add Stamp Rule**.
            Set its `StampName` to match a stamp your Forger emits (e.g.
            “House”, “Tree”, “Road”).

---

**`Step 4`**

Right-click again and add one or more **Prefab Nodes**
            (single prefab) or **Prefab Array Nodes** (uniform-random pick across N
            prefabs). Drag from the Stamp Rule's output port to each Prefab/Array's input port to
            connect them. Drop a prefab onto the ObjectField, set its `Probability`,
            and set `StopFlow` and `Static` as needed.

---

**`Step 5`**

Each Stamp Rule, Prefab Node, and Stamp Emitter has its own
            `PositionOffset`, `EulerOffset`, and `Scale` Vec3
            fields built directly into the card. Toggle the **Random** dice icon on
            any axis to switch from a fixed value to a Min/Max range — no separate Vector3
            node needed.

---

**`Step 6 (optional — recursion)`**

For child stamps: right-click the canvas and pick **Add Stamp
            Emitter → *name*** (the menu lists every existing Stamp Rule by
            name). The emitter appears with the name pre-set. Drag from a Prefab Node's *Emit*
            output to the emitter's input. After the parent prefab spawns at runtime, the engine
            fires a child stamp by that name — resolved to whichever Stamp Rule shares it,
            and spawned at every `ForgerMarker` child inside the parent prefab.

---

**`Step 7`**

Click away from the window or close it — the asset auto-saves.
            Drag the Stencil onto any Forger's **Stencils** array slot in the inspector
            and press **Build**. There is no import step or sidecar file.

---

!!! info
    **Multiple Stencils per Forger.** A single Forger can reference multiple Stencils.
            When generating, every Stencil's rules are searched in array order — the first
            Stencil holding a rule whose `StampName` matches the emitted stamp wins. Use
            this to layer a base Stencil with optional overrides (e.g. a "Halloween" Stencil that
            adds extra rules in front of the year-round one).

Stamp
#### Stamp Rule Node

The entry point for stencil resolution. Every unique stamp name emitted by a Forger
            needs a matching Stamp Rule. When the engine processes a stamp, it locates the rule whose
            `StampName` matches and evaluates its connected Prefab candidates.
Output Port:
```
Prefabs
```
— connects to one or more
                Prefab Nodes; the connected list becomes this rule's
```
PrefabChoices
```
Header field:
```
StampName
```
string— the stamp name to match (e.g. “House”). Renaming triggers a
                downstream invalidation so other Stencils referencing this name notice.Header toggle:
```
Enabled
```
bool— uncheck to mute the rule without deleting it (useful for A/B comparisons).Body Vec3 fields:
```
PositionOffset
```
,
```
EulerOffset
```
,
```
Scale
```
— rule-level transform offsets that
                stack on top of any prefab-level offsets at spawn time. Each axis can be a fixed
                value or a Min/Max random range — seeVec3 Fields.
Prefab
#### Prefab Node

Holds a candidate prefab and its spawn metadata. Multiple Prefab Nodes connected to one
            Stamp Rule create a weighted-random candidate pool. The card displays a live preview
            thumbnail rendered by Unity's `AssetPreview` service.

!!! info
    **What can be assigned to the Prefab field?**
    Any *GameObject asset* from the Project window:
    
    **Prefabs** (`.prefab`) — the typical case
    **Prefab Variants** (also `.prefab`) — behave identically
    **Model files** (`.fbx`, `.gltf`, `.obj`, `.dae`, …) — the imported root counts as a GameObject
    
    **Scene objects are not accepted.** The field is project-asset-only.
    *Heads up — model files spawn as read-only.* If you assign a `.fbx` directly and later need to attach a script, collider, or other component, the spawned instance won't accept it. Right-click the model in the Project window and run *Create → Prefab Variant*; assign the variant in place of the raw model.

Input Port:
```
Stamp
```
— from a Stamp Rule's outputHeader caret:click the ▾/▸ glyph in the title bar to
                collapse the body to just the title bar — useful for keeping large graphs
                tidy. The collapsed state is persisted on the asset.Body fields:- `Prefab` `GameObject` — the prefab to instantiate. Drag from the Project window onto the ObjectField.
- `Probability` `float ≥ 0` — relative weight inside the candidate pool. Default: 1.0
- `StopFlow` `bool` — if this candidate spawns, the engine stops rolling the rest of the pool
- `Static` `StaticFlag enum` — controls the static flag applied to the spawned GameObject and all of its children:
                        
**Unchanged** — leave the prefab asset's own static setting as-is (default)
**ForceStatic** — set `isStatic = true` on the instance and every child (batching / lighting / occlusion bakes)
**ForceNonStatic** — set `isStatic = false` on the instance and every child (useful when the source prefab asset is marked static but must spawn as a dynamic object)
- **Unchanged** — leave the prefab asset's own static setting as-is (default)
- **ForceStatic** — set `isStatic = true` on the instance and every child (batching / lighting / occlusion bakes)
- **ForceNonStatic** — set `isStatic = false` on the instance and every child (useful when the source prefab asset is marked static but must spawn as a dynamic object)
- `Ext. Managed` `bool` — when checked, the spawned instance is reparented out of the holder on rebuild instead of being destroyed. Use for NPCs or objects whose lifecycle is handed off to an external system (e.g. an NPC controller) after spawning.
- `Nav Static` `bool` — when checked, adds the **Navigation Static** editor flag to the spawned instance and all of its children so they are included in navmesh baking. No effect in player builds.
- `PositionOffset`, `EulerOffset`, `Scale` — per-prefab Vec3 offsets layered on top of the rule's offsets
- `UseCustomPreviewSettings` — opt in to per-node camera tuning. See Preview Settings.

Array
#### Prefab Array Node

A single card holding a *list* of prefabs. Picked by uniform random at spawn
            time. Use this when "any of these N props will do" — rocks, foliage, debris, building
            variants. One card replaces what would otherwise be a stack of identical Prefab Nodes.

!!! info
    **Accepted asset types:** the same as the Prefab Node — any GameObject
                    asset (Prefabs, Prefab Variants, or model files such as `.fbx` /
                    `.gltf` / `.obj`). Scene objects are not accepted.
                    See Prefab Node for the
                    full note about model files and Prefab Variants.

Input Port:from a Stamp Rule (left side)Output Port:"Emit" → connects to one or more Stamp Emitter nodes (right side)Body fields:- **PREFABS** sub-list — one row per prefab; click **+** to add an empty slot, drop a prefab onto its ObjectField. Click **×** to remove.
- `Weight` `float 0–1` — spawn probability shared by every member of the array. Default: 1.0
- `Stop Flow` / `Static` — same semantics as a single Prefab Node (see above), applied uniformly to every member of the array.
- `Ext. Managed` / `Nav Static` — same semantics as a single Prefab Node (see above), applied uniformly to every member of the array.
- `Position` / `Rotation` / `Scale` Vec3 fields — offsets layered onto each spawned member.

At compile time the array expands intoNindependent
```
WorldForgerPrefabChoice
```
records sharing the metadata fields above —
                runtime sees them as flat candidates of the connected Stamp Rule.
Emit
#### Stamp Emitter Node

The recursion piece. A small node placed *downstream* of a Prefab (or Prefab
            Array) that fires a child stamp by name after the parent spawns. By-name resolution
            keeps the visual graph acyclic — there's no edge between an emitter and its target
            Stamp Rule, even though runtime recursion can be arbitrarily deep.
Input Port:from a Prefab or Prefab Array's "Emit" outputNo Output Port:the emitter is a terminal node on the canvas; the
                actual recursion target is resolved by
```
StampName
```
match at compile time.Body fields:- `StampName` `string` (header) — the name of the child stamp to emit. Must match a `StampRuleNode.StampName` for any candidates to resolve. Also matched against `ForgerMarker.StampName` children of the parent prefab to choose the spawn position.
- `Position` / `Rotation` / `Scale` Vec3 fields — offsets layered onto the matched marker transform (or the parent transform if no marker matches) before each child spawns.

!!! info
    **Quick-pick UX:** right-click the canvas and you'll see **Add Stamp Emitter
                    → *name*** for every Stamp Rule already on the canvas. Picking one
                    creates an emitter pre-bound to that name. With no rules yet, the menu falls back
                    to a generic **Add Stamp Emitter Node**.

!!! info
    **Recursion limit:** the runtime enforces a hard depth cap of
                    **8 levels** (`WorldForgerEngine.MaxChildStampDepth`).
                    Anything deeper is silently dropped to prevent runaway recursion if an emitter
                    chain happens to loop. The cycle
                    detector will paint the offending Stamp Rules red before that's ever an issue.

!!! warning
    **Live-preview note:** emitter edits (rename, offsets, edge add/remove)
                    always route through `ChangeType.Structure` and trigger a full
                    `Forger.Build()`. The transform-only fast path tracks only top-level
                    spawned instances; per-child trackers are a planned follow-up.

Vec3
#### Vec3 Fields (inline)

Every `PositionOffset` / `EulerOffset` / `Scale` field
            on a Stamp Rule, Prefab, or Child Stamp is a tri-axis Vec3 control rendered directly
            inline on the card — there is no separate Vector3 or Random Vector3 node type. Each
            axis (X/Y/Z) toggles independently between a fixed value and a Min/Max random range.
Per-axis controls:- **Dice icon (☢):** click to toggle that axis between
                    *fixed* and *random* mode. The icon highlights when random.
- **Fixed mode:** a single number field. Edits ride the
                    *TransformOnly* live-preview fast path — existing instances reposition in place
                    with no respawn.
- **Random mode:** Min and Max number fields. Edits ride the
                    *RuleContent* fast path — the matrix is re-evaluated against the same
                    instance seed, so each instance jumps to its newly-rolled value without flicker.

Determinism:the random roll is seeded by the spawning instance's
```
EvaluationSeed
```
(the spatial salt at spawn time). The same Stencil + same
                Forger seed always produces the same per-instance rolls, so tweaking a Min/Max range
                is non-destructive — pressing Build with the same seed gives the same layout.
!!! tip
    **Example — Random Y rotation:** on a Prefab Node, click the dice
                    on the `EulerOffset` Y axis. Enter Min 0, Max 360. Leave X and Z
                    fixed at 0. Each spawned house now faces a random direction.

!!! tip
    **Example — Slight scale variation:** on a Stamp Rule's
                    `Scale`, click the dice on all three axes. Set Min 0.95, Max 1.05
                    for each. Every instance of that rule receives a 5 % size jitter on top of
                    its prefab's per-prefab scale.

### Live Preview

Live Preview lets you tune a Stencil with the graph editor open and see the active scene's
        Forger respond in real time. Toggle **Live** in the toolbar to enable it. Every
        edit is debounced for 300 ms, then routed to one of two paths depending on what changed.

### Change Tiers

`LivePreviewController` classifies each edit into one of three tiers
            (`ChangeType`). Within a debounce window, the controller never downgrades the
            pending tier — structure always wins.

**`TransformOnly`** · `Fast path`

Fixed-value drags on a `PositionOffset` /
                `EulerOffset` / `Scale` Vec3 axis — on a Stamp Rule, Prefab,
                Prefab Array, *or* Stamp Emitter node. The controller walks every
                `ForgerStampInstance` tracker in the scene and re-poses it in place using the
                new offset, then walks every `ForgerChildStampInstance` tracker in ascending
                depth order so the entire child-stamp chain follows along — no respawn, no flicker.

---

**`RuleContent`** · `Fast path`

Random-mode toggles (the dice icon) and Min/Max range edits.
                The matrix re-evaluates against each instance's stored seed, so values jump to
                their newly-rolled results without disturbing the GameObject identity. Rides the
                same fast path as TransformOnly.

---

**`Structure`** · `Slow path`

Anything that changes *which* prefab spawns,
                *how many*, or under what conditions: prefab swap, probability,
                `StopFlow`, `Static` (StaticFlag), edge add/remove, rule add/remove,
                stamp-name rename, adding/removing a
                Spawn Filter. Triggers
                a full `Forger.Build()` using an in-memory Stencil derived from the
                current graph.

---

### Seed Pinning

On the first slow-path build of a Live session, the controller captures the Forger's
            `EffectiveSeed` and reuses it for every subsequent rebuild. This keeps the
            spatial layout consistent while you tweak rules — you're seeing the same village,
            with one variable changing. Reassigning the asset (or closing/reopening the window)
            resets the pinned seed.

### Per-Instance Tracker

Every top-level GameObject the engine spawns receives a
            `ForgerStampInstance` component recording the originating stamp's world
            transform, the rule and choice GUIDs, and the spatial-salt seed used for its random
            rolls. Each child stamp the engine spawns through a `ForgerMarker` socket (or
            via pivot-to-pivot chaining) receives a `ForgerChildStampInstance` component
            instead, recording its parent instance, marker-local matrix, depth in the chain, and the
            emitter / rule / choice GUIDs. The fast path processes both tiers in ascending depth
            order so every parent's transform is up-to-date before its children re-evaluate. See
            ForgerStampInstance and
            ForgerChildStampInstance
            for the field-level reference.

!!! warning
    **Limitations.** The fast path only re-poses *top-level* spawned
            instances. `ChildStamps` emitted via `ForgerMarker` sockets do
            *not* carry trackers — their transforms update on the next full Build. If your
            scene predates the tracker (was built before this engine version shipped), the first
            TransformOnly edit will fall through to a full rebuild silently; subsequent edits are then
            on the fast path.

!!! tip
    **Apply button.** The **Apply** toolbar button force-flushes any
            pending change immediately, bypassing the 300 ms debounce. Useful for slider drags
            where you want every intermediate value reflected in the scene.

### Sticky Notes

Sticky notes are free-floating annotations on the canvas. They have no runtime effect —
        they exist purely so designers can leave inline comments on the graph (TODOs, balance notes,
        "tweak this for variety", etc.). Add one via right-click → **Add Sticky
        Note**.

Selecting a sticky note opens its inspector pane on the right with two foldable sections,
        **Identity** (Title + multi-line Contents) and **Appearance**
        (Theme + Font Size dropdowns). All four fields can also be edited inline on the canvas, but
        the inspector is friendlier for paragraph-length notes and discoverable for the
        right-click-only theme / font-size options.

**`Title / Contents`**

Click the title bar on the canvas to rename, or click the body to
            edit inline. Both fields are also editable from the inspector — Title is a single-line
            text field; Contents is a multi-line growable text area suitable for paragraphs. Both
            persist on the asset (`StickyNoteData.Title` /
            `StickyNoteData.Contents`).

---

**`Theme`** · `Classic / Black`

Pickable from the inspector's Appearance section, or via right-click
            on the canvas note. Maps to
            `UnityEditor.Experimental.GraphView.StickyNoteTheme` (0 = Classic,
            1 = Black).

---

**`Font Size`** · `Small / Medium / Large / Huge`

Pickable from the inspector's Appearance section, or via right-click
            on the canvas note. Stored as an integer (0–3) on
            `StickyNoteData.FontSize`.

---

**`Resize / Move`**

Sticky notes are resizable by dragging the bottom-right corner and
            movable by dragging the title bar. Position and size persist. Selecting a note and
            pressing ++delete++ removes it.

---

!!! info
    **Search includes notes.** The toolbar Search field matches sticky-note titles
            as well as stamp/prefab names, so a note titled "TODO: Halloween" is findable from the
            same search box used to navigate the graph.

### Groups

Groups are named frames that visually cluster related nodes on the canvas. Like sticky notes
        they have *no* runtime effect — they exist purely to help organise large stencils.
        Moving a group's frame moves every node inside it together. Create one via right-click →
        **Create Group**, or by selecting nodes and choosing **Group Selection**.

Selecting a group frame opens its inspector pane on the right, with three foldable sections:
        **Identity**, **Appearance**, and **Members**.

### Identity

**`Title`** · `string`

Editable label shown in the group's canvas header. Renaming in the
            inspector updates the on-canvas title live without reloading the graph. Also editable
            inline by double-clicking the header text on the canvas.

---

### Appearance

**`Background`** · `Color`

Optional tint applied to the group frame on the canvas. Useful for
            visually grouping clusters by category — for example all "Houses" wirings in green,
            all "Specialised Buildings" in blue. The picker hides the alpha slider so you can't
            accidentally save an invisible colour.

---

**`Title`** · `Color`

Optional override for the group title text colour. Use this when a
            strongly tinted background makes the default light-grey title hard to read — pick a
            contrasting colour to keep the header legible.

---

**`Reset to Default`**

Clears both colour overrides at once and restores the GraphView's
            built-in colours. Use the alpha-0 sentinel internally so re-saved assets serialise cleanly
            with no override data when you've reset.

---

### Members

**`Tree view`**

A read-only outline of the nodes inside the group, organised by their
            edge connections. Stamp Rules sit at the top level; their connected Prefab and Prefab Array
            cards appear indented under them; any Stamp Emitters hanging off those prefab cards
            appear one level deeper. Members with no in-group parent (e.g. a lone Prefab Array node
            grouped on its own) appear as roots.

Each row shows the node's kind (Stamp Rule / Prefab / Prefab Array
            / Stamp Emitter) plus its primary identifier — the stamp name for rules and emitters,
            the prefab name for single Prefab cards, and "*N* prefabs — *first*, …" for arrays.
            Useful for auditing a group's contents at a glance without scanning the canvas.

---

!!! info
    **Foldout state persists per group.** Each group remembers its Identity /
            Appearance / Members section's expanded-or-collapsed state independently in
            `EditorPrefs`, so you can keep Members collapsed on most groups and expanded on
            the one you're auditing.

### Validation

The graph editor flags configuration mistakes inline so you don't have to dig through the
        scene to find why a stamp isn't spawning. Validators run on every edit, not just on Build.

**`Orphan Prefab`** · `amber outline`

A Prefab Node with no incoming edge has nothing to spawn it. The
            card paints an amber border and a tooltip on the input port reads "No Stamp Rule
            connects to this Prefab." Connect an edge from a Stamp Rule to clear it.

---

**`Empty Stamp Rule`** · `amber outline`

A Stamp Rule with no Prefab candidates does nothing at runtime —
            the engine simply emits the stamp and finds no matching choice. The card paints an
            amber border. Connect at least one Prefab to clear it.

---

**`Missing Prefab Reference`** · `red ring`

A Prefab Node whose `Prefab` ObjectField is empty (or
            references a deleted asset) paints a red ring around the field. The runtime would
            silently skip this candidate at spawn time.

---

**`Duplicate Stamp Name`** · `amber border on title`

Two Stamp Rules sharing the same `StampName` means only
            the first match wins at lookup time. The duplicates show an amber title bar with a
            tooltip naming the conflict. Rename one or merge the rules.

---

!!! tip
    **Validation is non-blocking.** You can still save and Build with warnings
            present — they're advisory. The amber/red colours match the project-wide debug-colour
            scheme used elsewhere in the toolkit (warn / error).

### Runtime Engine

The `WorldForgerEngine` is the runtime interpreter that resolves stamps into
        instantiated prefabs. It processes every stamp emitted by a Forger against the assigned
        Stencils.

### Resolution Algorithm

**`1. Match Stamp`**

For each emitted stamp, the engine searches the Forger's
                Stencils in array order for a `WorldForgerStampRule` whose
                `StampName` matches. The first match wins.

---

**`2. Spatial Salt`**

A spatial salt is computed from the stamp's position. The
                Forger's seed is XOR'd with this salt to produce an `EvaluationSeed` that
                drives every random decision for this single placement.

---

**`3. Weighted Roll`**

The rule's `PrefabChoices` are walked in connection
                order. Each candidate's `Probability` is rolled against the
                spatially-seeded random; the first to succeed becomes the spawn target. If
                `StopFlow` is true on the winner, the remaining candidates are skipped.

---

**`4. Compose Matrix`**

The final world matrix is
                `TRS(stamp) * TRS(rule offset) * TRS(choice offset)`. Vec3 fields in
                random mode roll their Min/Max range against the same
                `EvaluationSeed` — deterministic across runs.

---

**`5. Instantiate & Tag`**

The prefab is instantiated under the Forger's holder. A
                `ForgerStampInstance` tracker is added to the top-level instance
                recording the stamp transform, rule GUID, choice GUID, seed, and
                `ExternallyManaged` flag — so Live Preview can re-pose without
                rebuilding and `Forger.Demolish()` can rescue managed instances.

---

**`6. Child Recursion`**

If the chosen prefab has `ChildStamps` defined and
                contains `ForgerMarker` children whose `StampName` matches,
                the engine recursively resolves each child stamp. Each child instance receives a
                `ForgerChildStampInstance` tracker recording its parent, depth,
                marker-local matrix, and emitter / rule / choice GUIDs — so the entire chain
                participates in the Live Preview fast path. Maximum recursion depth:
                **8 levels** (`WorldForgerEngine.MaxChildStampDepth`).

---

!!! info
    **Stencil order matters.** Stencils on a Forger are searched array-first; the
            earliest Stencil with a matching `StampName` wins. Layer overrides (e.g. a
            seasonal Stencil) at index 0 and the base Stencil at index 1.

### ForgerMarker Component

`ForgerMarker` is a lightweight component you add to child GameObjects inside
        a prefab to define **child-stamp sockets** — positions where the
        engine can recursively spawn additional themed objects.

**`StampName`** · `string`

The name of the child stamp this socket represents. Must match the
            `StampName` on a Child Stamp entry inside the parent Prefab Node, AND a
            corresponding Stamp Rule somewhere in the Forger's Stencils.

---

### Workflow Example

Suppose you have a “House” prefab and want to place random chimney variations on
            its roof:
- Open the House prefab and create an empty child GameObject at the chimney position
- Add a `ForgerMarker` component and set `StampName` to “Chimney”
- In your Stencil, on the House Prefab Node, click **+** under *Child Stamps* and add an entry named “Chimney”
- Add a separate Stamp Rule with `StampName` = “Chimney” and connect chimney Prefab Nodes to it

At generation time, the engine spawns a House, finds the ForgerMarker, emits a fresh
            "Chimney" stamp at the marker's transform, and resolves it through the Chimney Stamp
            Rule — placing a randomly chosen chimney at the marked position.

!!! tip
    **Tip:** You can place multiple ForgerMarkers with different stamp names inside a
            single prefab. A house could have sockets for “Chimney”, “Door”, and
            “WindowBox” — each resolved independently.

### ForgerStampInstance Component

`ForgerStampInstance` is a tracker component automatically added by the engine
        to every *top-level* GameObject it spawns. It records what produced this instance
        so the Live Preview fast path can recompose the world matrix without rebuilding.

### Field Reference

**`StampPos / StampRot / StampScale`** · `Vector3 / Quaternion / Vector3`

The *original stamp transform* the Forger emitted —
                position, rotation, and scale before any rule or prefab offset. The fast path
                rebuilds the matrix as
                `TRS(stamp) * TRS(rule offset) * TRS(choice offset)`; only the second
                two factors change when you tweak Vec3 fields, so this stays constant for the
                life of the instance.

---

**`RuleGuid / ChoiceGuid`** · `string`

Stable identifiers (`StampRuleNodeData.Guid` /
                `PrefabNodeData.Guid`) the live-preview controller uses to look up the
                current rule and choice from the editing Stencil. If either GUID no longer
                matches (e.g. you deleted the rule), the instance is left alone until the next
                full Build.

---

**`EvaluationSeed`** · `int`

The spatially-salted seed used for this instance's random
                rolls. Re-rolling against the same seed produces the same Min/Max value, so
                random Vec3 edits look stable when previewed live.

---

**`ExternallyManaged`** · `bool`

Mirrors the `Ext. Managed` flag on the originating
                Prefab / Prefab Array node. When `true`, `Forger.Demolish()`
                reparents the instance out of the holder before destroying the holder, so the
                GameObject survives a rebuild. Use for NPCs or any object whose lifecycle is owned
                by an external system after spawning.

---

!!! warning
    **Don't edit by hand.** The component is marked
            `[DisallowMultipleComponent]` and its values are written by the engine on
            spawn. Modifying fields manually breaks the fast path's lookup — the instance will
            revert on the next Live Preview tick.

!!! info
    **Child stamps have their own tracker.** The top-level instance gets
            `ForgerStampInstance`; every child stamp the engine spawns (marker-based or
            pivot-to-pivot) gets a `ForgerChildStampInstance` instead. Both tiers are walked
            by the Live Preview fast path so an offset edit on a Stamp Emitter node deep in the chain
            re-poses every existing instance without a full rebuild. See
            ForgerChildStampInstance.

### ForgerChildStampInstance Component

`ForgerChildStampInstance` is the child-stamp counterpart to
        `ForgerStampInstance`. The engine adds it to every GameObject spawned by
        `ProcessChildStamps` — whether the child landed on a
        `ForgerMarker` socket or chained pivot-to-pivot from its parent — so the
        Live Preview fast path can recompose the child's world matrix from the live graph without a
        full `Forger.Build()`.

### Matrix Composition

For each tracker the fast path computes:

```
socketMatrix = parentFinalWorld * markerLocalMatrix   (marker-based)
            or parentFinalWorld                        (pivot-to-pivot)

final = socketMatrix
      * emitterOffset(EvaluationSeed)   // StampEmitterNodeData offsets
      * choiceOffset(EvaluationSeed)    // WorldForgerPrefabChoice offsets
```

`parentFinalWorld` is read directly from `ParentInstance.transform`.
            The fast path processes trackers in ascending `Depth` order so the parent's
            transform has already been updated in the same tick before any child reads it.

### Field Reference

**`Depth`** · `int`

`1` for a direct child of a top-level stamp,
                `2` for a grandchild, and so on. Capped at
                `WorldForgerEngine.MaxChildStampDepth` (8). The fast path uses this to
                sort updates so parents are always re-posed before children.

---

**`ParentInstance`** · `GameObject`

The spawned GameObject one level up the chain. Carries
                `ForgerStampInstance` when `Depth == 1`, otherwise another
                `ForgerChildStampInstance`.

---

**`UsesMarker`** · `bool`

`true` if a `ForgerMarker` socket on the
                parent prefab was used to place this instance — the
                `MarkerLocal*` fields then store that marker's transform in the parent
                prefab's local space. `false` for pivot-to-pivot chaining, in which case
                the marker fields are unused and the parent's final world matrix is the socket
                directly.

---

**`MarkerLocalPos / MarkerLocalRot / MarkerLocalScale`** · `Vector3 / Quaternion / Vector3`

Captured at spawn time from
                `parent.transform.worldToLocalMatrix * markerWorldMatrix`. Reusing these
                instead of re-querying the marker each tick lets the fast path survive cases where
                the marker GameObject has been disabled or moved by another system.

---

**`EmitterNodeGuid`** · `string`

GUID of the `StampEmitterNodeData` that defined this
                child-stamp slot. Used by the fast path to look up the emitter's current
                `PositionOffset` / `EulerOffset` / `Scale` via
                `WorldForgerGraphAsset.TryGetEmitterNode`.

---

**`ChildRuleGuid / ChildChoiceGuid`** · `string`

GUIDs of the Stamp Rule the child resolved to (by name match)
                and the Prefab Node selected from its candidate pool. Used together with
                `WorldForgerGraphAsset.TryGetRuleAndChoice` to read the choice's current
                offsets.

---

**`EvaluationSeed`** · `int`

The seed passed to `WorldForgerVector3.Evaluate` at
                spawn time. Reusing it keeps random offset rolls deterministic across fast-path
                ticks.

---

!!! warning
    **Don't edit by hand.** Same caveat as
            `ForgerStampInstance` — the component is
            `[DisallowMultipleComponent]` and is overwritten on every spawn. Manual edits
            revert on the next Live Preview tick.

### Custom Spawn Filters

A **spawn filter** is a designer-authored ScriptableObject that runs every
        time the engine is about to spawn one of your prefabs. Each filter gets to make one of
        three decisions:
- **Reject the spawn** — "don't place a tree here, there's already one within 3 m"
- **Modify the world transform** — "snap this fence post to align with the terrain normal"
- **Post-process the spawned GameObject** — "after this barrel spawns, attach a Rigidbody to it"

Filters are attached to **Prefab** and **Prefab Array** nodes in
        the Stencil Graph. They run in list order; the first `TryAccept` rejection
        cancels the spawn entirely. Multiple filters on one node compose — e.g. drop both
        a `MinDistance` and an `AlignToTerrain` filter on the same Tree node
        and the engine first rejects spawns that are too close, then aligns the survivors to the
        ground.

### When to use a filter (vs. another mechanism)

**`Use a filter when…`**

The decision depends on context that isn't part of the
                stencil itself: terrain slope, distance to other spawned objects, layer-mask checks,
                day/night state, save data. Filters get a live `ForgerSpawnContext` and
                can read whatever scene data they need.

---

**`Don't reach for a filter when…`**

A simpler primitive already exists. Random scale variation?
                Use the **random** mode on the Vec3 field. Spawn this prefab less
                often? Lower its **Probability**. Stop spawning siblings once one
                hits? Use **StopFlow**. Filters are for *conditional / contextual*
                logic that can't be expressed as static parameters.

---

### Authoring workflow — three steps

**Step 1.** Write a C# class that inherits from
            `ForgerSpawnFilter`. Override one or more of the five virtual methods (all
            are optional). Add a `[CreateAssetMenu]` attribute so the asset shows up in
            `Assets → Create`.

```
using UnityEngine;
using B2C3D.WorldForger;

[CreateAssetMenu(menuName = "World Forger/Filters/Min Distance")]
public class MinDistanceFilter : ForgerSpawnFilter
{
    public float MinDistance = 3f;

    public override bool TryAccept(ForgerSpawnContext ctx)
    {
        Vector3 pos = ctx.ProposedPosition;
        foreach (Transform child in ctx.Holder)
            if (Vector3.Distance(child.position, pos) < MinDistance)
                return false;   // reject — too close
        return true;            // accept
    }
}
```

!!! info
    **Performance note — the snippet above is illustrative, not production-ready.**
                Walking `ctx.Holder` on every spawn attempt is `O(N)` per call, so a
                full build is `O(N²)` in the spawn count. Fine for ~50 buildings; visibly slow
                past a few thousand. For production, use the spatial-hash pattern: allocate a uniform-grid
                `Dictionary<Vector3Int, List<Vector3>>` in `OnBuildStart`
                with cell size equal to `MinDistance`, record each accepted spawn in
                `OnInstantiated`, and only consult the 9 (2D) or 27 (3D) neighbouring cells
                in `TryAccept`. That collapses each call to roughly constant time. The
                shipping `MinDistanceFilter.cs` is implemented exactly this way — read
                it for the full reference pattern.

**Step 2.** Right-click in the Project window and run
            `Create → World Forger → Filters → Min Distance`. This
            creates a `.asset` file holding one configured copy of the filter. You can
            create as many as you want, each with its own values:

```
Assets/Filters/
├─ TreeMinDist3m.asset      (MinDistance = 3, used on Tree nodes)
├─ HouseMinDist8m.asset     (MinDistance = 8, used on House nodes)
└─ TowerMinDist15m.asset    (MinDistance = 15, used on Tower nodes)
```

**Step 3.** Open the Stencil Graph, find the Prefab Node (or Prefab Array
            Node) you want to gate, and look for the **FILTERS** section near the
            bottom of the card. Click `+` to add an empty slot, then drag your filter
            asset onto it. The same asset can be referenced from many nodes — editing the
            asset's values updates every node that uses it.

!!! info
    **One class, many configured assets.** The C# class defines the
                *behaviour*. Each `.asset` file is one *configured instance*.
                That means one `MinDistanceFilter.cs` can produce
                `TreeMinDist3m.asset`, `HouseMinDist8m.asset`,
                `TowerMinDist15m.asset` — same code, different values.

**Step 4 (optional) — Custom icon.** If you want your filter asset
            to show a distinctive icon in the Project window (matching the visual language of the
            stock filters), drop a 64×64 PNG anywhere in the project and call
            `IconRegistry.TryAssign<T>(iconFileName)` from a small editor-only
            `[InitializeOnLoad]` shim. The lookup is path-free — it finds the
            icon by file name and the script by type, then writes the binding into the script's
            `.meta` file (so it survives moving either the icon or the script):

```
using B2C3D.WorldForger.Editor;
using UnityEditor;

[InitializeOnLoad]
internal static class MyFilterIconBinding
{
    static MyFilterIconBinding()
    {
        EditorApplication.delayCall += () =>
            IconRegistry.TryAssign<MinDistanceFilter>("MinDistanceFilter");
    }
}
```

The first argument is the C# type, the second is the icon's file name without
            extension. Place the shim in any editor-only assembly (an `Editor`
            subfolder, or any asmdef with `"includePlatforms": ["Editor"]`).
            `TryAssign` is idempotent — safe to call on every domain reload, only
            re-imports when the binding actually changes.

### Filter Hooks — what each method does

**`OnBuildStart(Transform holder)`** · `virtual void`

Called once at the start of every
                `Forger.Build()`, before any candidate is processed. Use this to
                initialise per-build state — clear a spatial hash, snapshot the terrain,
                allocate buffers. Default: no-op. The same `holder` Transform will
                be passed to every `ForgerSpawnContext` during this build.

---

**`TryAccept(ForgerSpawnContext ctx) → bool`** · `virtual bool`

Decide whether to allow this candidate to spawn. Return
                `false` to reject — the engine then continues to the next sibling
                candidate (or stops, if a `StopFlow` would have applied). Filters in
                the list run in order; the FIRST `false` short-circuits the rest.
                Default: returns `true`.

---

**`ModifyTransform(ForgerSpawnContext ctx) → Matrix4x4`** · `virtual Matrix4x4`

Modify the world transform before instantiation. Each filter
                receives the previous filter's output as `ctx.ProposedTransform`, so
                multiple filters chain (e.g. `SnapToGrid` →
                `AlignToNormal`). Return `ctx.ProposedTransform` unchanged
                to leave the transform alone. Default: returns
                `ctx.ProposedTransform`.

---

**`OnInstantiated(GameObject instance, ForgerSpawnContext ctx)`** · `virtual void`

Called once per spawn after the prefab has been instantiated,
                its world transform applied, the live-preview tracker attached, and any
                child-stamp recursion completed. Use for component additions
                (`AddComponent<Rigidbody>`), layer changes, registering the
                instance with an external system, etc. Default: no-op.

---

**`OnBuildEnd(Transform holder)`** · `virtual void`

Called once at the end of every `Forger.Build()`,
                after every stamp has been processed. Always fires — even if the build
                throws — so any state you allocated in `OnBuildStart` can be
                released here. Default: no-op.

---

### Hook order, per spawn

For each candidate that passes its probability roll, the engine walks the filter list
            three times:
1. **Pass 1 — Selection.** Walk filters → the first
            `TryAccept` returning `false` cancels the spawn (engine moves on
            to the next sibling).
2. **Pass 2 — Transform modification.** Walk filters →
            `ModifyTransform` chains, each filter seeing the previous filter's output
            via `ctx.ProposedTransform`.
3. **Engine instantiates the prefab**, applies the (possibly modified)
            transform, attaches trackers, applies static / nav-static flags, and recurses into
            child stamps.
4. **Pass 3 — Post-instantiation.** Walk filters →
            `OnInstantiated` for any cleanup or augmentation. By this point the spawned
            subtree is fully built, so a filter that calls
            `SetLayerRecursively(instance.transform, layer)` covers every child stamp
            too.

### ForgerSpawnContext — what filters see

A read-only struct passed by value to every hook. Fields:

**`Stamp`** · `WorldForgerStamp`

The originating top-level stamp emitted by the Forger
                (`StampName`, world `Position` /
                `Rotation` / `Scale`, optional
                `Metadata`). Always non-null — even at deep child-stamp depths,
                this still references the original top-level stamp for traceability.

---

**`Rule`** · `WorldForgerStampRule`

The Stamp Rule that resolved this candidate — gives
                access to the rule's stamp name, sibling candidates, and rule-level offsets.
                For child-stamp spawns this is still the originating top-level rule (use
                `Depth` to tell which level of the chain you're at).

---

**`Choice`** · `WorldForgerPrefabChoice`

The specific Prefab Choice the engine is about to spawn:
                `Prefab` reference, probability, flags
                (`StaticMode` / `ExternallyManaged` /
                `AffectsNavigation`), and the child stamps it will emit. A single
                shared filter asset can branch on `ctx.Choice.Prefab` for per-prefab
                logic.

---

**`ProposedTransform`** · `Matrix4x4`

The world matrix the engine intends to use, already composed
                from stamp × rule offset × choice offset (and, for child stamps,
                marker-local × emitter offset × choice offset). Convenience getters:
                `ProposedPosition`, `ProposedRotation`,
                `ProposedScale`.

---

**`Depth`** · `int`

`0` for top-level stamps; `1` for direct
                children spawned through a `ForgerMarker` socket or pivot-to-pivot
                chaining; `2` for grandchildren; capped at
                `WorldForgerEngine.MaxChildStampDepth` (8). A filter that should only
                affect top-level placements can early-out on `ctx.Depth != 0`.

---

**`Seed`** · `int`

The spatially-salted seed used for this instance's random
                rolls. Filters that need their own deterministic random (jitter that survives
                rebuilds with the same Forger seed) should derive a `System.Random`
                from this rather than from `UnityEngine.Random`.

---

**`Holder`** · `Transform`

The Forger's output holder Transform — every
                already-spawned sibling in this build is one of its descendants, which is how
                `MinDistance`-style spatial queries work. Climb to
                `holder.parent` to reach the Forger itself if you need scene-level
                state.

---

### Where the values live — one class, many assets

Configuration lives on the `.asset` file, not on the node. So if you want
            a 3 m minimum distance for trees and an 8 m minimum for houses, you create
            *two* asset files from the same `MinDistanceFilter` class, each
            with its own value, and drop the appropriate one onto each node. Asset files are
            ~200 bytes each — cheap, version-controlled, and discoverable in the Project view.

For more elaborate cases (one asset that switches behaviour based on which prefab
            is spawning), branch on `ctx.Choice.Prefab` inside the filter:

```
[CreateAssetMenu(menuName = "World Forger/Filters/Min Distance (Per-Prefab)")]
public class MinDistancePerPrefabFilter : ForgerSpawnFilter
{
    [System.Serializable] public class PrefabRule {
        public GameObject Prefab;
        public float      MinDistance;
    }

    public float DefaultMinDistance = 3f;
    public List<PrefabRule> Overrides = new();

    public override bool TryAccept(ForgerSpawnContext ctx) {
        float minDist = DefaultMinDistance;
        foreach (var o in Overrides)
            if (o.Prefab == ctx.Choice.Prefab) { minDist = o.MinDistance; break; }
        // ... distance check using minDist
    }
}
```

### Prefab Array Node — shared filters

The filter list on a Prefab Array Node is **shared metadata** —
            every member of the array runs through the same filter chain. This matches how
            `StaticMode`, `ExternallyManaged`, and
            `AffectsNavigation` are shared across the array.
            `WorldForgerGraphAsset.RebuildPrefabArrayCompiledChoices` copies the
            list (by reference) into every compiled `WorldForgerPrefabChoice` at
            `Compile()` time.

If you need different filters per array member, split the array into individual
            Prefab Nodes — each then has its own filter list.

### Live Preview interaction

Filters run during the **slow path** only — that is, inside
            `WorldForgerEngine.Apply` during a full `Forger.Build()`. The
            **fast path**
            (Live Preview's
            `TryApplyTransformOnly`) only re-poses already-spawned instances and does
            *not* re-run filters — selection decisions were locked in at the
            original spawn.

Adding or removing a filter on a node fires `ChangeType.Structure`, which
            triggers a full rebuild — correct, since filters change *which* instances
            spawn. Editing parameters *inside* a filter asset (e.g. raising
            `MinDistance` from 3 to 5) is outside the graph and does *not*
            trigger Live Preview automatically. To re-evaluate, click **Apply** in
            the toolbar.

### Build lifecycle

`Forger.Build()` walks every rule in every assigned Stencil, collects
            every unique `ForgerSpawnFilter` referenced by any
            `WorldForgerPrefabChoice.SpawnFilters` list, and dedupes via a
            `HashSet<ForgerSpawnFilter>`. Each unique filter receives exactly
            one `OnBuildStart` call and exactly one `OnBuildEnd` call per
            build, regardless of how many nodes reference it.

`OnBuildEnd` fires unconditionally inside a `finally` block, so
            a filter that allocates resources in `OnBuildStart` can release them even
            if the engine throws.

### Determinism

Filter logic should be a pure function of `ForgerSpawnContext` plus the
            filter's own configured fields. Any randomness should be seeded from
            `ctx.Seed` — not `UnityEngine.Random` — so a rebuild
            with the same Forger seed produces identical output. The seed is already
            spatially-salted at this point, so two stamps at different positions get independent
            random sequences automatically.

!!! info
    **Stock filters ship in the box.** See
            Stock Filters for
            `MinDistanceFilter`, `MaxSlopeFilter`,
            `HeightRangeFilter`, `AlignToTerrainNormalFilter`, and
            `SnapToGridFilter` — each is a complete
            `ForgerSpawnFilter` subclass you can create assets from directly via
            `Assets → Create → World Forger → Filters → ...`,
            no scripting required.

### Stock Filters

World Forger ships with five ready-to-use `ForgerSpawnFilter` subclasses
        covering the common spatial-constraint cases. Right-click in the Project window and
        choose `Create → World Forger → Filters → [name]` to make
        configured asset instances, then drop them onto Prefab / Prefab Array nodes.

All five live under `Assets/B2C3D/WorldForger/Runtime/Filters/Stock/`.
        Read their source for a worked example of how to author your own filters —
        `MinDistanceFilter.cs` in particular shows the
        `OnBuildStart` / `OnInstantiated` / `OnBuildEnd`
        lifecycle pattern for spatial-hash state.
MinDistanceFilter
### MinDistanceFilter

Rejects a spawn when any previously-accepted sibling in the same build is closer
            than a configurable distance. Backed by a uniform-grid spatial hash so it stays
            fast on village-scale rebuilds (no O(N²) scan). The hash is allocated in
            `OnBuildStart` and released in `OnBuildEnd`.

"Sibling" means another spawn that *also* ran through this same
            filter asset. Drop the same asset onto every node that should respect each
            other; the asset is shared so they all consult and update the same hash.

**`MinDistance`** · `float`

Minimum world-space distance between this spawn and any
                already-accepted sibling. Spawns closer than this are rejected. Default 3.

---

**`IgnoreYAxis`** · `bool`

When true (default), only X/Z components are used —
                two objects on different terraces count as separated. Set false for full 3D
                distance checks (caves, towers, multi-story builds).

---
MaxSlopeFilter
### MaxSlopeFilter

Rejects a spawn when the ground slope at the proposed position is steeper than
            the configured angle. Use for content that should only land on relatively-flat
            ground — houses, market stalls, paved tiles. Casts one ray straight down
            through the chosen `GroundLayers` and compares the hit normal to
            world up.

**`MaxSlopeAngle`** · `float (0–90)`

Maximum allowed angle between the ground normal and
                world up, in degrees. 0 = perfectly flat only; 90 = any slope including
                walls. Default 15.

---

**`GroundLayers`** · `LayerMask`

Which collider layers count as ground. Include your
                Unity Terrain layer (the TerrainCollider sits on layer 0 by default) and
                any mesh-collider terrain layers. Default Everything.

---

**`RayHeight / RayLength`** · `float / float`

Origin height (above proposed position) and total
                length of the downward ray. Defaults 50 / 200 cover most village-scale
                terrain.

---

**`RejectIfNoGround`** · `bool`

When true (default), reject if the ray hits nothing.
                Set false if your scene has stamps that legitimately float above empty space.

---
HeightRangeFilter
### HeightRangeFilter

Rejects a spawn whose Y position is outside `[MinHeight, MaxHeight]`.
            Useful for biome-style gating: reeds only near sea level, snowy pines only above
            80 m, lanterns only between 0–3 m off the ground.

**`Source`** · `enum (ProposedPosition / RaycastDown)`

`ProposedPosition` reads Y straight off the
                stamp — cheap, right when the Forger emits stamps already at the
                surface. `RaycastDown` casts a ray and uses the actual ground Y
                — right when stamps are emitted at a fixed height (e.g. y=0).

---

**`MinHeight / MaxHeight`** · `float / float`

Inclusive bounds (world space).

---

**`GroundLayers / RayHeight / RayLength / RejectIfNoGround`** · `LayerMask / float / float / bool`

Raycast settings — only consulted when
                `Source = RaycastDown`. Same semantics as the matching fields on
                `MaxSlopeFilter`.

---
AlignToTerrainNormalFilter
### AlignToTerrainNormalFilter

Tilts the proposed rotation so the prefab's local up direction matches the
            terrain normal at the spawn position. Original yaw is preserved — only
            pitch and roll change. This is the only stock filter that hooks
            `ModifyTransform` rather than `TryAccept`.

If the downward ray misses ground, the filter is a no-op and returns the
            proposed transform unchanged. Pair with `MaxSlopeFilter` or a
            `RaycastDown`-mode `HeightRangeFilter` if you need
            placements without ground to be rejected.

**`GroundLayers / RayHeight / RayLength`** · `LayerMask / float / float`

Same semantics as `MaxSlopeFilter`.

---

**`Strength`** · `float (0–1)`

0 = no effect; 1 = full alignment. Slerps between the
                original and target rotation, so mid values give a partial lean toward the
                slope — often more natural for short props on shallow grades.

---
SnapToGridFilter
### SnapToGridFilter

Snaps the proposed position to the nearest cell of a uniform grid. Useful for
            cobblestones, road segments, modular building blocks — any content
            authored on a fixed grid where stencil offsets would otherwise break alignment.
            Rotation and scale pass through untouched.

**`CellSize`** · `Vector3`

Cell size per axis. Set X=2, Y=0, Z=2 for a 2 m
                horizontal grid that leaves Y free. Values ≤ 0 disable snapping on that
                axis regardless of the boolean flags.

---

**`Origin`** · `Vector3`

Grid lines pass through this world-space point. Use
                to align the grid to an off-zero reference (e.g. centre cells over (1,0,1)).

---

**`SnapX / SnapY / SnapZ`** · `bool / bool / bool`

Per-axis enable. Default `true / false / true`
                — horizontal snap, terrain-following Y.

---

!!! info
    **Stacking patterns.**
    
    **Houses on flat, well-spaced ground:**
    `MinDistanceFilter(8) + MaxSlopeFilter(15°)`
    **Trees with terrain-following lean:**
    `MinDistanceFilter(2) + AlignToTerrainNormalFilter(Strength = 0.4)`
    **Cobblestone tiles snapped to a grid:**
    `SnapToGridFilter(CellSize = 1) + MaxSlopeFilter(5°)`
    **Reeds at sea level only:**
    `HeightRangeFilter(0–0.5)`
    **Snowy pines on a high alpine biome:**
    `HeightRangeFilter(80–200) + MinDistanceFilter(5)`

### Extending WorldForger

The **Editor Tools framework** lets you (or third-party asset-pack
        authors) add toolbar buttons, right-click menu items, validation rules, inspector
        buttons, and graph exporters to WorldForger *without modifying its source
        code*. Everything is reflection-discovered at editor load time, so dropping
        a script into your project is the only setup required — no manifest, no
        registration call, no settings file.

### The five plug points

Each plug point is a pair: an `[Attribute]` that marks a class as
            discoverable, plus an `abstract` base class your subclass extends.
            The framework scans every loaded assembly via Unity's
            `TypeCache.GetTypesWithAttribute<T>`, finds your subclasses,
            instantiates them once, and routes invocations.

**`[ForgerStencilGraphTool]`** · `extends ForgerStencilGraphTool`

A button under the Stencil Graph window's
                **Tools** dropdown. Receives the active asset and graph
                view; mutate the asset, frame nodes, etc. Grouped by Category.

---

**`[ForgerNodeContextMenu(typeof(...))]`** · `extends ForgerNodeContextMenu`

A right-click menu item that appears *only* on
                graph nodes whose data type matches the target type
                (`PrefabNodeData`, `StampRuleNodeData`, etc.).
                Optional `IsAvailable` override grays the item out
                conditionally.

---

**`[ForgerGraphValidator]`** · `extends ForgerGraphValidator`

A diagnostic that runs when the user clicks the
                **Validate** button. Walks the asset, appends issues with
                severity (Info/Warning/Error) and optional node GUIDs. Issues with a
                node GUID are click-to-frame in the results popup.

---

**`[ForgerInspectorTool(typeof(...))]`** · `extends ForgerInspectorTool`

A button on a Forger's component inspector.
                Polymorphic targeting: `typeof(Forger)` appears on every
                Forger subclass; `typeof(VillageForger)` only on VillageForger;
                a third-party `typeof(MyDungeonForger)` only on their
                Forger.

---

**`[ForgerExporter]`** · `extends ForgerExporter`

A custom export format. Appears under the
                **Tools → Export** submenu. The framework prompts for
                a save path (filtered by your declared file extension) and calls your
                `Export(asset, path)`. Throw on I/O errors — the
                framework catches and shows a dialog.

---

### Authoring workflow — minimal example

**Step 1.** Create your own assembly definition (highly
            recommended for asset-pack authors), or drop the script into the project's
            default Editor folder. Reference `Forge.Editor.asmdef`.

```
// MyAssetPack.Editor.asmdef
{
  "name": "MyAssetPack.Editor",
  "references": [
    "Forge.Editor",
    "Forge.Runtime"
  ],
  "includePlatforms": ["Editor"]
}
```

**Step 2.** Write a class and decorate it with the appropriate
            attribute. No further wiring needed:

```
using UnityEditor;
using UnityEngine;
using B2C3D.WorldForger;
using B2C3D.WorldForger.Editor;

[ForgerStencilGraphTool(Category = "My Asset Pack", DisplayName = "Set All Probabilities to 1.0")]
public class SetProbabilitiesToOneTool : ForgerStencilGraphTool
{
    public override void OnInvoke(WorldForgerGraphAsset asset, WorldForgerGraphView view)
    {
        Undo.RecordObject(asset, "Set Probabilities");
        foreach (var n in asset.PrefabNodes)
            if (n?.Choice != null) n.Choice.Probability = 1f;
        EditorUtility.SetDirty(asset);
    }
}
```

**Step 3.** Save. Unity recompiles. The next time you open a
            Stencil Graph, your tool appears under **Tools → My Asset Pack
            → Set All Probabilities to 1.0**. No Asset Store download has
            opinions about it — it's just a class in your project.

### Cross-assembly discovery — how it actually finds you

`ForgerToolRegistry` uses `UnityEditor.TypeCache` —
            an indexed cache Unity maintains across the entire editor domain. It does
            *not* walk individual asmdefs or care which assembly you put your
            tool in; the index covers *everything* Unity has loaded. The only
            requirement is that your assembly is loaded (true for any asmdef in the
            project) and that your class has the right attribute.

On `AssemblyReloadEvents.afterAssemblyReload` the registry
            invalidates its cache, so editing or adding a tool produces an updated
            menu on the very next interaction — no editor restart, no domain
            reload prompt.

**Asset pack distribution.** When a buyer drops your asset
            pack into their project, every `[ForgerStencilGraphTool]` /
            `[ForgerInspectorTool]` / etc. you ship auto-appears in the
            relevant menus. No setup screen, no integration step. That's the headline
            value of the framework.

### Polymorphic Forger targeting — the killer feature

`[ForgerInspectorTool]` takes a Forger type. The framework walks
            the inheritance chain so:

```
// Appears on every Forger — VillageForger, PrefabForger, future DungeonForger…
[ForgerInspectorTool(typeof(Forger), DisplayName = "Save Build As Prefab")]
public class SaveAsPrefabTool : ForgerInspectorTool { ... }

// Appears only on VillageForger (its inheritance chain includes Forger).
[ForgerInspectorTool(typeof(VillageForger), DisplayName = "Regenerate Roads Only")]
public class RegenerateRoadsTool : ForgerInspectorTool { ... }

// A third-party asset-pack ships a DungeonForger AND its tools; tools
// appear only on the DungeonForger inspector, naturally scoped.
[ForgerInspectorTool(typeof(MyDungeonForger), DisplayName = "Bake Per-Room Lighting")]
public class BakeRoomLightingTool : ForgerInspectorTool { ... }
```

The same dispatch machinery handles
            `[ForgerNodeContextMenu(typeof(NodeData))]` — menu items
            scope to a specific node type so the right-click menu doesn't bloat as more
            tools land.

### Hooking into existing custom editors

For Forger subclasses with *no* custom editor, the framework's
            `ForgerEditor` auto-applies via
            `[CustomEditor(typeof(Forger), editorForChildClasses: true, isFallback: true)]`
            and draws the default Inspector plus your tools. No work needed.

For Forger subclasses *with* their own custom editor (e.g.
            `VillageForgerEditor`, `PrefabForgerEditor`), Unity's
            polymorphic-editor dispatch claims the subclass before the framework's
            fallback. Add a single line at the end of your custom editor's
            `OnInspectorGUI` to surface the tool buttons:

```
public override void OnInspectorGUI()
{
    // ... your existing UI ...

    // Append framework tool buttons for this Forger's runtime type.
    ForgerInspectorToolsDrawer.Draw((Forger)target);
}
```

One line, no more thinking required. The drawer renders nothing when no
            tools target this Forger type, so it's safe to add even when you have no
            tools yet.

### Stock examples that ship

The package ships five concrete tools under
            `Editor/Tools/Stock/` — one per plug point. Read their
            source for worked examples:
- `FindEmptyPrefabsTool` — `ForgerStencilGraphTool`
                that logs and frames Prefab Nodes / Array slots with no prefab assigned.
- `FindOrphanNodesTool` — `ForgerStencilGraphTool`
                that walks edges to find nodes with no incoming/outgoing connections.
- `EmptyPrefabsValidator` — `ForgerGraphValidator`
                version of the empty-prefab check, surfaced via the Validate button.
- `JsonGraphExporter` — `ForgerExporter` using
                `JsonUtility` for a quick textual snapshot.
- `SelectPrefabInProjectMenu` —
                `ForgerNodeContextMenu` targeting `PrefabNodeData`
                — pings the referenced asset.
- `CopyEffectiveSeedTool` —
                `ForgerInspectorTool` targeting `Forger` —
                copies the last build's seed to the system clipboard.

### Exception isolation — why a buggy tool can't crash the editor

Every framework call into your code is wrapped in `try/catch`.
            Exceptions are logged via `Debug.LogException` with the offending
            tool's name, and (for major hooks like Export and StencilGraphTool) surfaced
            in a Unity dialog so the user knows which tool to blame. Other tools and the
            editor itself are unaffected.

The same applies to *instantiation*: if your tool's constructor throws
            (e.g. you forgot a parameterless ctor), the registry skips it with an error
            log, and every other tool still loads. There is never a "one bad tool brings
            down all tools" failure mode.

### Tool authoring checklist
1. The class is **not abstract**.
2. The class has a **public parameterless constructor**
                (auto-generated when you don't declare one).
3. The class is decorated with the appropriate attribute
                (`[ForgerStencilGraphTool]`, etc.).
4. The class extends the matching abstract base
                (`ForgerStencilGraphTool`, etc.).
5. The required virtual methods are overridden.
6. The script lives in an Editor assembly (an Editor folder, an asmdef
                with `"includePlatforms": ["Editor"]`, or both).
7. The assembly references `Forge.Editor.asmdef`.

Failing any of items 1–5 produces a clear error in the Console
            naming your type. Failing items 6–7 produces a compile error.

!!! info
    **Asset Store packaging note.** When you publish a third-party
            WorldForger extension to the Asset Store, your tool classes need to land in an
            assembly that loads *after* WorldForger's. The standard pattern: ship
            an Editor asmdef under your folder that references `Forge.Editor`.
            Buyers drop your package in, recompile happens, your tools auto-appear —
            the same flow as any user-authored tool above. No special setup. No "enable
            plugin" step.

### Spatial Salting

Spatial salting is the randomization strategy that ensures every placement location makes
        independent random decisions, preventing “all or nothing” patterns.

### How It Works

Before evaluating probability rolls at each stamp position, the engine computes a
            **spatial hash** from the stamp’s grid coordinates:

salt = (ix * 73856) ^ (iz * 19349)

This salt is combined with the global **Seed** to initialize the random state
            for that position. The result: two adjacent houses will roll different probabilities, even
            though they share the same stamp name and Stencil. Changing the seed produces an
            entirely different layout while preserving determinism — the same seed always
            generates the same result.

!!! info
    **Deterministic Generation:** Because randomization is seeded, runs are fully
            reproducible. The same Seed + same layout = identical output every time. Use the
            **Randomize** button to quickly explore variations.

### Preview Settings

Prefab Nodes render a live thumbnail of the assigned prefab on the card. By default the
        thumbnail uses Unity's built-in `AssetPreview` service. Each Prefab can opt in
        to a custom camera setup if the auto-framing clips or poorly frames your prefab.

**`UseCustomPreviewSettings`** · `bool`

Toggle on the Prefab inspector to override the default thumbnail
            with a custom camera. When OFF, Unity's `AssetPreview` draws the thumbnail
            and the slider values below it are ignored (but remain visible and editable).

---

**`CustomPreviewSettings`** · `WorldForgerPreviewSettings`

Per-node camera distance, pitch/yaw angle, and pivot offset.
            Settings are persisted on the asset and are cosmetic only — they do not affect
            generation.

---

!!! tip
    **Tip:** The Preview Settings header is collapsible — click the ▾/▸
            caret to fold the section away once you've dialled the camera in. All sliders stay visible
            while expanded regardless of the *Use Custom* toggle, so you can tune values first
            and flip the toggle when you're ready.

!!! tip
    **Tip:** Preview settings are per-node, so different prefabs in the same graph
            can have individually tuned camera angles for the best visual reference while editing.

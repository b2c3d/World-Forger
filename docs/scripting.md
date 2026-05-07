### Runtime API & Events

Every Forger exposes a small, build-safe scripting surface so you can kick off generation from
        gameplay code, react when a build finishes, and inspect timing and seed data after the fact.
        This is the foundation for on-screen UI demos, procedural worlds that rebuild during play, and
        automated test harnesses.

!!! info
    **Build-safety guarantee.** The Runtime assembly contains *zero* direct
            `UnityEditor.*` references at call sites. All editor-only helpers (Undo registration,
            prefab-connection preservation) are funnelled through an internal helper whose bodies compile
            to empty no-ops in player builds. You can drop a `VillageForger` or
            `PrefabForger` into any Windows / macOS / Linux / mobile standalone build without
            stripping, `#if` gating, or custom link files.

### Kicking off a build from code

`Forger.Build()` and `Forger.Demolish()` are both `public`
            and runtime-safe. You can call them from any MonoBehaviour on any frame. The base class also
            exposes `AutoBuildOnStart` (serialized `bool`) for scenes that want a
            generate-on-spawn behaviour without writing glue code.

[SerializeField] private VillageForger _forger;

public void OnGenerateButton() => _forger.Build();
public void OnClearButton()    => _forger.Demolish();

### Lifecycle Events (C# event )

For programmatic subscribers, the base `Forger` class fires four C# events. Use
            these from code that doesn’t live in the scene inspector.

**`ForgeStarted`** · `event Action<Forger>`

Fires *just before* generation begins, inside the
                `try` block. Useful for disabling the Generate button, showing a progress
                spinner, or dimming the UI.

---

**`ForgeCompleted`** · `event Action<ForgeResult>`

Fires after a successful generation. The argument carries the
                effective seed, stamp count, total milliseconds, and the holder GameObject. See
                *ForgeResult* below.

---

**`ForgeFailed`** · `event Action<Forger, string>`

Fires if `Build()` throws. The second argument is the
                exception message. The exception is also logged via `Debug.LogException`, so
                the stack trace remains visible in the Console — but the throw itself is caught,
                so an unhandled exception can never crash the caller.

---

**`Demolished`** · `event Action<Forger>`

Fires after `Demolish()` removes the holder. Called once
                per demolish, including the implicit demolish that runs at the start of
                `Build()`.

---

### Lifecycle Events (Inspector UnityEvent )

The same four lifecycle moments are also exposed as serialized `UnityEvent`s under
            the **Events** header in the Forger inspector. Drag a target GameObject in,
            pick a method from the dropdown, and you’ve wired a reaction with zero code. Ideal for
            demo scenes, UGUI buttons, and VFX triggers.

**`OnForgeStarted`** · `UnityEvent<Forger>`

Inspector mirror of `ForgeStarted`.

---

**`OnForgeCompleted`** · `UnityEvent<ForgeResult>`

Inspector mirror of `ForgeCompleted`. The
                `ForgeResult` is passed to listeners that accept it; listeners that take no
                argument are called without one.

---

**`OnForgeFailed`** · `UnityEvent<Forger, string>`

Inspector mirror of `ForgeFailed`.

---

**`OnDemolished`** · `UnityEvent<Forger>`

Inspector mirror of `Demolished`.

---

### ForgeResult struct

`ForgeResult` is the payload published by `ForgeCompleted` /
            `OnForgeCompleted`, and also cached on `Forger.LastResult` so any code
            can query the most recent outcome.

**`Forger`** · `Forger`

The Forger that produced this result. Handy when one listener
                subscribes to multiple Forgers.

---

**`EffectiveSeed`** · `int`

The seed actually used for this run. Equals `Forger.Seed`
                when that field was non-zero; otherwise the randomly chosen value that would otherwise
                be invisible. Copy this to reproduce a layout later.

---

**`StampsEmitted`** · `int`

Number of stamps the Forger pushed to the engine before spawning.
                Useful as a quick “how big was this village?” metric.

---

**`TotalMs`** · `float`

Wall-clock duration of the entire `Build()` call in
                milliseconds, captured with `System.Diagnostics.Stopwatch`. Show this in an
                on-screen HUD to let viewers compare seed complexity.

---

**`Holder`** · `GameObject`

The parent GameObject under which spawned prefabs live. Null on
                failure. Use it to pan the camera, parent FX, or tag the generated content.

---

**`Success`** · `bool`

`true` if the run completed without throwing.

---

**`FailureReason`** · `string`

When `Success` is `false`, holds the caught
                exception’s message. `null` on success.

---

### LastResult property

`Forger.LastResult` returns the most recent `ForgeResult`. It is
            updated on both success and failure, so callers that arrive after generation can query it
            without subscribing to events.

var r = _forger.LastResult;
if (r.Success)
    Debug.Log($"Seed {r.EffectiveSeed} produced {r.StampsEmitted} stamps in {r.TotalMs:F1} ms");

### Full subscription example

A typical HUD controller subscribes in `OnEnable` and unsubscribes in
            `OnDisable`. Using `+=` / `-=` (rather than the inspector
            UnityEvent) keeps the wiring in source control and lets you share one listener across
            multiple Forgers.

using UnityEngine;
using UnityEngine.UI;
using B2C3D.WorldForger;

public class VillageHud : MonoBehaviour
{
    [SerializeField] private VillageForger _forger;
    [SerializeField] private Button        _generateButton;
    [SerializeField] private Text          _statusLabel;

    void OnEnable()
    {
        _generateButton.onClick.AddListener(_forger.Build);
        _forger.ForgeStarted   += HandleStarted;
        _forger.ForgeCompleted += HandleCompleted;
        _forger.ForgeFailed    += HandleFailed;
    }

    void OnDisable()
    {
        _generateButton.onClick.RemoveListener(_forger.Build);
        _forger.ForgeStarted   -= HandleStarted;
        _forger.ForgeCompleted -= HandleCompleted;
        _forger.ForgeFailed    -= HandleFailed;
    }

    void HandleStarted(Forger f)
    {
        _generateButton.interactable = false;
        _statusLabel.text            = "Generating…";
    }

    void HandleCompleted(ForgeResult r)
    {
        _generateButton.interactable = true;
        _statusLabel.text            = $"Seed {r.EffectiveSeed} • {r.StampsEmitted} stamps • {r.TotalMs:F0} ms";
    }

    void HandleFailed(Forger f, string reason)
    {
        _generateButton.interactable = true;
        _statusLabel.text            = $"Failed: {reason}";
    }
}

!!! info
    **Demo-scene wiring without code.** For a pure-inspector demo, you can skip the
            script above entirely: drag the Forger into a UGUI `Button.OnClick` entry and pick
            `Forger.Build`; then wire `OnForgeCompleted` on the Forger itself to a
            `Text.text` setter for a status readout, or to an `Animator` trigger for a
            celebratory flourish. No `#if UNITY_EDITOR`, no compile step — ships as-is in a
            standalone player.

!!! info
    **Runtime config mutation is a Phase 2 feature.** Changing
            `VillageForgerConfig` or `VillageForgerProfile` fields at runtime
            *works* (they are plain `ScriptableObject` / `MonoBehaviour`
            instances) but mutating the same shared Profile asset from a built player also persists in the
            editor during Play mode. For safe live-config UIs, clone the Profile into a runtime copy before
            editing. A first-class `ApplyProfile(runtimeCopy)` helper and a
            `ForgerRuntimeController` MonoBehaviour are planned for Phase 2.

### Stencil Graph Builder

`StencilGraphBuilder` is an editor-only fluent API for authoring stencil graphs from
        C# — a higher-level alternative to opening the Graph editor and wiring nodes by hand.
        It wraps the raw node-data lists (StampRules, PrefabNodes, PrefabArrayNodes, StampEmitters,
        Edges) so you can map prefabs to stamp names without managing GUIDs, edge records, or canvas
        positions.

!!! info
    **Editor-only.** Lives in
            `B2C3D.WorldForger.Editor.Authoring`. Don't ship this assembly with player builds —
            it's a tool for authoring stencil *assets*, not a runtime API.

### Typical usage

Open a fresh or existing `WorldForgerGraphAsset`, chain the wirings you want,
            and call `Save()`. The same builder instance can be reused across many calls in
            the same authoring session.

using B2C3D.WorldForger;
using B2C3D.WorldForger.Editor.Authoring;

var asset = AssetDatabase.LoadAssetAtPath<WorldForgerGraphAsset>(path);

StencilGraphBuilder.Open(asset)
    .EnsureRule("VillageChurch")
    .SetStamp("VillageChurch", new[] { church1, church2 })   // weighted array
    .SetStamp("VillageInn",    tavern)                        // single prefab
    .SetStamp("VillageWell",   wells, opts => {
        opts.AffectsNavigation = true;
        opts.PositionOffset    = Vector3.up * 0.1f;
    })
    .ClearStamp("VillageGround")
    .RemoveOrphans()
    .Save();

### API reference

**`Open(asset)`** · `static StencilGraphBuilder`

Creates a builder bound to `asset`. Subsequent method
            calls mutate this asset in place; use `Save()` to commit to disk.

---

**`EnsureRule(stampName, opts)`** · `StencilGraphBuilder`

Ensures a Stamp Rule node with the given name exists. No-op when the
            rule is already present. Optional `StampRuleOptions` set Enabled / Position /
            Euler / Scale on the rule when freshly created.

---

**`SetStamp(stampName, GameObject prefab, opts)`** · `StencilGraphBuilder`

Wires *one* prefab as the only candidate for the named stamp.
            Replaces any existing wiring for this stamp (upsert). Creates a Stamp Rule for the stamp
            if missing. The prefab is wrapped in a `PrefabNodeData`; pass
            `PrefabChoiceOptions` to set probability / static flag / offsets.

---

**`SetStamp(stampName, IEnumerable<GameObject> prefabs, opts)`** · `StencilGraphBuilder`

Wires a weighted *array* of candidates — uniform random
            selection at spawn time. Creates a single `PrefabArrayNodeData` sharing one set
            of `PrefabChoiceOptions` across every member. Replaces any existing wiring for
            the named stamp.

---

**`ClearStamp(stampName)`** · `StencilGraphBuilder`

Removes all prefab wiring for the named stamp — drops the rule's
            outgoing edges and any prefab-side cards exclusively used by this rule. The rule itself
            stays in place so its name keeps appearing in stamp-name pickers. Cards shared with other
            rules are preserved (only the targeted rule's edge is dropped).

---

**`RemoveRule(stampName)`** · `StencilGraphBuilder`

Stronger than `ClearStamp` — removes the rule node
            entirely along with its wiring.

---

**`AddChildStamp(parentStamp, childStamp, opts)`** · `StencilGraphBuilder`

Adds a Stamp Emitter downstream of every prefab wired to
            `parentStamp`'s rule. Each spawned parent prefab will then emit
            `childStamp` as a child stamp at runtime. The child's rule must also exist in
            this stencil — call `EnsureRule(childStamp)` first if you're building from
            scratch. Optional `EmitterOptions` set the per-emitter offsets layered on top
            of the marker / parent transform.

---

**`RemoveOrphans()`** · `StencilGraphBuilder`

Drops any edge whose source or target GUID doesn't resolve to an
            existing node. Useful after manual asset editing or after removing nodes by hand.

---

**`Validate()`** · `IReadOnlyList<string>`

Returns a (possibly empty) list of human-readable warnings about the
            current stencil state — rules with no wiring, prefab nodes with null prefabs,
            arrays with all-null entries, emitters whose target rule doesn't exist. Read-only; does
            not modify the asset. Useful for build-pipeline assertions.

---

**`Save()`** · `void`

Commits any pending in-memory edits to disk via
            `AssetDatabase.SaveAssetIfDirty` and invalidates the runtime rule-lookup cache
            so the next `GetRuleForStamp` call rebuilds from the new edges. No-op if no
            builder method has modified the asset since the last `Save`.

---

### Option classes

Three lightweight POCOs configure the optional parameters on the builder methods. Each
            defaults to the same values the corresponding node-data class uses, so passing a
            zero-config `opts` reproduces the data-class defaults exactly.

**`PrefabChoiceOptions`**

Per-prefab options — `Probability`,
            `StopFlow`, `StaticMode` (StaticFlag), `ExternallyManaged`,
            `AffectsNavigation`, `PositionOffset` / `EulerOffset` /
            `Scale` (Vector3). Applies to `SetStamp` overloads.

---

**`StampRuleOptions`**

Rule-level options — `Enabled` (bool),
            `PositionOffset` / `EulerOffset` / `Scale` applied at
            the rule level (sums with prefab-level offsets at spawn time). Applies to
            `EnsureRule`.

---

**`EmitterOptions`**

Per-emitter offsets layered on top of the marker / parent transform
            when the child stamp fires. Applies to `AddChildStamp`.

---

!!! info
    **Mutation semantics.** Each method writes through to the in-memory asset
            immediately so subsequent calls in the same chain see the new state.
            `Save()` commits to disk — if you don't call it, your edits are still in
            memory but won't survive a domain reload. Wrap a builder session in your own
            `Undo.RecordObject` scope before the first call if you want undo / redo to roll
            back the whole batch as a single step.

!!! info
    **Layout.** Newly-created Prefab / Prefab Array cards land 60 px to the right of
            their parent rule. New Stamp Rule cards stack vertically below any existing rules so they
            don't overlap. Matches the manual graph view's left-to-right reading convention so a
            builder-authored stencil opens cleanly in the editor.

### Forger Plugin Architecture

World Forger discovers `Forger` subclasses through a small attribute-based plugin
        contract. Adding a new Forger type — yours or a third-party's — is a matter of writing a
        `Forger` subclass, decorating it with `[ForgerPlugin(...)]`, and
        shipping the usual editor pieces. Unity's `TypeCache` picks the type up
        automatically across asmdefs, so registration is zero-config: install the package, the
        plugin shows up.

!!! info
    **What ships first-party.** The Village Forger and the Prefab Forger are both
            registered through this contract — they're concrete plugins, not hardcoded built-ins. Look at
            their attribute declarations as worked examples.

### The contract — three pieces

A complete Forger plugin is:
1. A concrete `Forger` subclass decorated with `[ForgerPlugin(...)]`
            (provides the metadata Welcome / pickers / future Forger-Browser surfaces consume).
2. A custom `UnityEditor.Editor` targeting that subclass — same pattern as any
            normal Unity component editor. The plugin system doesn't replace this; you still write
            an inspector if you want a non-default one.
3. (Optional) A `[MenuItem("GameObject/World Forger/Create <Name>")]`
            helper for one-click GameObject creation. Unity's `[MenuItem]` requires
            compile-time-constant paths, so the registry can't auto-generate menu items — but the
            registry-driven UI (Welcome window cards, pickers, the Forger-side Browser if present)
            lights up regardless of whether you ship a menu item.

### The attribute

`ForgerPluginAttribute` lives in `B2C3D.WorldForger` (the runtime
            assembly) so plugins can apply it without taking an editor dependency. It carries pure
            metadata — there's no runtime cost, the editor reads it through
            `TypeCache.GetTypesWithAttribute<ForgerPluginAttribute>()`.

[ForgerPlugin(
    DisplayName         = "Village Forger",
    Tagline             = "Procedural villages with road generation and building placement.",
    Description         = "Generates a complete village from a Village Profile asset...",
    IconName            = "VillageForgerBanner",
    DocumentationAnchor = "village-forger",
    Order               = 10)]
public class VillageForger : Forger { /* ... */ }

### Attribute fields

**`DisplayName`** · `string`

Human-readable name shown on Welcome window cards, future picker UIs,
            and any other registry-driven surface. Falls back to the type's short name when null.

---

**`Tagline`** · `string`

One-line summary suitable for a card subtitle.

---

**`Description`** · `string`

Multi-paragraph long-form description shown when the plugin's card
            is selected on the Welcome window's Forgers tab.

---

**`IconName`** · `string`

Filename (without extension) of a banner / icon texture, resolved
            through the project's `IconRegistry`. The icon can live anywhere under
            `Assets/` as long as its name is unique. Recommended size: 600 × 200 PNG with
            transparency.

---

**`DocumentationAnchor`** · `string`

An HTML anchor in `WorldForgerHelp.html`
            (e.g. `"village-forger"`) when your plugin documents itself in the bundled
            manual, OR a full `https://...` URL when it ships its own external docs. The
            "Open Documentation" button on the plugin's Welcome card jumps to whichever you provide.

---

**`Order`** · `int`

Sort order across all registered plugins (lower = earlier). Default
            is `1000`, so first-party plugins (Village = 10, Prefab = 20) lead and
            third-party plugins fall in afterwards unless they set their own explicit order.

---

### Discovery — TypeCache

The editor-side `ForgerPluginRegistry` queries Unity's `TypeCache`
            on first access — Unity pre-computes that cache during domain reload, so the lookup is
            effectively free. Crucially it works *across asmdef boundaries*: your plugin can
            ship in its own asmdef referencing `B2C3D.WorldForger.Runtime` and the registry
            picks it up the moment the editor finishes compiling. No `[InitializeOnLoad]`
            registration call, no manifest, no rebuild step.

using B2C3D.WorldForger.Editor;

foreach (var plugin in ForgerPluginRegistry.All)
    Debug.Log($"{plugin.DisplayName} ({plugin.Type.FullName})");

// Or look up a specific Forger
var info = ForgerPluginRegistry.Get<VillageForger>();

### What the registry drives
- **Welcome window's Forgers tab** — cards iterate the registry; the
            "Add to Scene" button uses `plugin.Type` to add the right component.
- **Pickers** that need to enumerate Forger types (e.g. a future Forger
            Browser, the Variant Generator's target dropdown).
- Anywhere else the codebase needs to enumerate Forger types — replaces every previous
            "hardcoded list of Village + Prefab" branch.

### What the registry doesn't drive
- **Top-level menu items.** Unity's `[MenuItem]` attribute
            requires compile-time-constant paths, so each plugin still ships its own
            `[MenuItem("GameObject/World Forger/Create <Name>")]` declaration. This
            isn't a regression — it's a Unity API constraint — and it's a single line of editor code
            per plugin.
- **Per-Forger inspector editors.** Continue writing
            `UnityEditor.Editor` subclasses with `[CustomEditor(typeof(MyForger))]`
            the standard way. The plugin system doesn't replace Unity's editor-discovery contract.
- **Profiles, configs, and other plugin-specific assets.** If your Forger
            wants its own `ScriptableObject` profile (like
            `VillageForgerProfile`), define and ship it however you want — the plugin
            contract doesn't enforce a profile shape.

!!! info
    **Coming-soon teasers.** The Welcome window's Forgers tab also supports
            *teaser entries* — coming-soon cards with no runtime type yet. They live as a small
            static array in `WorldForgerWelcomeWindow` alongside the registry-driven entries
            so the marketing surface can preview future Forgers (e.g. a Dungeon Forger) before the actual
            type ships. When the type arrives, decorate it with `[ForgerPlugin]` and remove
            the teaser entry — that's the whole conversion.

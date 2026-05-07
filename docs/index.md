---
hide:
  - navigation
  - toc
---

![World Forger](images/WorldForgerBanner.png)

# World Forger

**Procedural Architecture & Environment Suite for Unity 6**

World Forger is a decoupled procedural generation engine that separates layout logic from visual theming. Layouts emit abstract **Stamps** which are resolved into prefabs by **Stencils** — giving level designers and technical artists the freedom to work independently.

---

<div class="grid cards" markdown>

-   :material-map-marker-outline: **Village Forger**

    High-level layout engine that generates organic, grid-based settlements with road networks, building placement, terrain conforming, and obstacle avoidance.

    [:octicons-arrow-right-24: Village Forger](village-forger.md)

-   :material-tune: **Village Profile**

    The shared "DNA" of a village — road rules, building definitions, debug colors, and diagnostics. Easily shared across multiple Forger instances.

    [:octicons-arrow-right-24: Village Profile](village-profile.md)

-   :material-cube-outline: **Prefab Forger**

    Micro-forger for individual themed objects. Drop it on any GameObject to resolve a single named stamp into a prefab from your Stencil.

    [:octicons-arrow-right-24: Prefab Forger](prefab-forger.md)

-   :material-graph: **Stencil Graph**

    Node-based editor for mapping stamp names to prefabs. Supports weighted random selection, spawn filters, live preview, and runtime generation.

    [:octicons-arrow-right-24: Stencil Graph](stencil-graph.md)

-   :material-tools: **Tools**

    Profile Browser, Stencil Graph Browser, and Variant Generator — purpose-built editors for exploring and iterating on your world configurations.

    [:octicons-arrow-right-24: Tools](tools.md)

-   :material-code-braces: **Scripting**

    Runtime API, UnityEvents, Stencil Graph Builder, and the Forger Plugin Architecture for extending World Forger with custom Forger types.

    [:octicons-arrow-right-24: Scripting](scripting.md)

-   :material-cog-outline: **Advanced**

    Spline integration, obstacle avoidance, and output tracking via the ForgerOutput marker system.

    [:octicons-arrow-right-24: Advanced](advanced.md)

-   :material-rocket-launch-outline: **Getting Started**

    Requirements, folder structure, core concepts, the generation pipeline, and resolution explained.

    [:octicons-arrow-right-24: Getting Started](getting-started.md)

</div>

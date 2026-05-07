"""
WorldForger HTML → MkDocs Markdown converter.
Reads WorldForgerHelp.html and produces 8 .md files in docs/.
Run: python convert.py
"""

import re
import os
from bs4 import BeautifulSoup, Tag, NavigableString

HTML_SRC = r"D:\Unity\Projects\B2C3D\Assets\B2C3D\WorldForger\Documentation\WorldForgerHelp.html"
OUT_DIR  = r"D:\Unity\Store Assets\World Forger Documentation Repo\docs"

# Map section IDs to output pages
PAGE_MAP = {
    "index.md": [
        "overview","requirements","folder-structure","core-concepts","pipeline","cell-size"
    ],
    "village-forger.md": [
        "village-forger","vf-theme","vf-build-settings","vf-actions","vf-scene-handles"
    ],
    "village-profile.md": [
        "village-profile","vp-grid","vp-market","vp-ground","vp-obstacles",
        "vp-main-roads","vp-side-roads","vp-residential","vp-specialized",
        "vp-colors","vp-overlay-shader","vp-diagnostics","vp-naming","vp-faq"
    ],
    "prefab-forger.md": [
        "prefab-forger","pf-theme","pf-stamp","pf-build-settings","pf-actions"
    ],
    "stencil-graph.md": [
        "theme-engine","te-graph-editor","te-inspecting-nodes","te-toolbar",
        "te-shortcuts","te-creating-themes","te-stamp-node","te-prefab-node",
        "te-prefab-array-node","te-stamp-emitter-node","te-vector-nodes",
        "te-live-preview","te-sticky-notes","te-groups","te-validation",
        "te-runtime-engine","te-forger-marker","te-stamp-instance",
        "te-child-stamp-instance","te-spawn-filters","te-stock-filters",
        "te-extending","te-spatial-salting","te-preview"
    ],
    "tools.md": [
        "profile-browser","stencil-graph-browser","variant-generator"
    ],
    "scripting.md": [
        "runtime-api","stencil-graph-builder","forger-plugins"
    ],
    "advanced.md": [
        "spline-integration","obstacle-avoidance","forger-output"
    ],
}

# HTML entities and special chars
ENTITIES = {
    "&rarr;": "→", "&larr;": "←", "&mdash;": "—", "&ndash;": "–",
    "&rsquo;": "'", "&lsquo;": "'", "&rdquo;": '"', "&ldquo;": '"',
    "&times;": "×", "&middot;": "·", "&amp;": "&", "&nbsp;": " ",
    "&gt;": ">", "&lt;": "<", "&#8594;": "→", "&#x2192;": "→",
}

def fix_entities(text):
    for ent, rep in ENTITIES.items():
        text = text.replace(ent, rep)
    # Numeric entities
    text = re.sub(r'&amp;', '&', text)
    return text

def get_text(el):
    """Get clean text from an element."""
    if el is None:
        return ""
    return fix_entities(el.get_text(separator=" ", strip=True))

def has_class(el, cls):
    return cls in (el.get("class") or [])

def convert_inline(el):
    """Convert an element's children to inline Markdown."""
    if el is None:
        return ""
    parts = []
    for child in el.children:
        if isinstance(child, NavigableString):
            parts.append(fix_entities(str(child)))
        elif isinstance(child, Tag):
            tag = child.name
            inner = convert_inline(child)
            if tag == "strong" or tag == "b":
                parts.append(f"**{inner.strip()}**")
            elif tag == "em" or tag == "i":
                parts.append(f"*{inner.strip()}*")
            elif tag == "code":
                parts.append(f"`{inner}`")
            elif tag == "kbd":
                parts.append(f"++{inner.lower().replace(' ', '+')}++")
            elif tag == "a":
                href = child.get("href", "")
                if href.startswith("#"):
                    parts.append(inner)  # internal anchor — drop for now
                else:
                    parts.append(f"[{inner}]({href})")
            elif tag == "span":
                if has_class(child, "btn-preview"):
                    parts.append(f"**[{inner}]**")
                elif has_class(child, "prop-type"):
                    parts.append(f"`{inner}`")
                else:
                    parts.append(inner)
            elif tag in ("br",):
                parts.append("  \n")
            else:
                parts.append(inner)
    return "".join(parts)

def convert_element(el, depth=0):
    """Convert a single element to Markdown lines."""
    lines = []

    if isinstance(el, NavigableString):
        text = fix_entities(str(el)).strip()
        if text:
            lines.append(text)
        return lines

    if not isinstance(el, Tag):
        return lines

    tag = el.name
    classes = el.get("class") or []

    # ── Section header ──────────────────────────────────────
    if has_class(el, "section-header"):
        h = el.find(["h2","h3","h4"])
        if h:
            level = int(h.name[1]) + 1  # h2→##, h3→###
            lines.append(f"\n{'#' * level} {get_text(h)}\n")
        return lines

    # ── Chapter title ────────────────────────────────────────
    if has_class(el, "chapter-title"):
        lines.append(f"\n# {get_text(el)}\n")
        return lines

    # ── Chapter intro ────────────────────────────────────────
    if has_class(el, "chapter-intro"):
        lines.append(f"\n{convert_inline(el).strip()}\n")
        return lines

    # ── chapter-banner (image) ───────────────────────────────
    if has_class(el, "chapter-banner"):
        img = el.find("img")
        if img:
            alt = img.get("alt", "")
            # We'll skip the actual image path since it's a relative Unity path
            lines.append(f"\n<!-- banner: {alt} -->\n")
        return lines

    # ── Property entry ───────────────────────────────────────
    if has_class(el, "prop"):
        label_el = el.find(class_="prop-label")
        body_el  = el.find(class_="prop-body")
        if label_el and body_el:
            # Get label text, stripping any btn-preview spans
            label_raw = label_el.get_text(strip=True)
            type_el   = body_el.find(class_="prop-type")
            type_str  = f" · `{get_text(type_el)}`" if type_el else ""
            desc_els  = body_el.find_all(class_="prop-desc")
            def_el    = body_el.find(class_="prop-default")

            lines.append(f"\n**`{label_raw}`**{type_str}\n")
            for desc in desc_els:
                lines.append(f"\n{convert_inline(desc).strip()}\n")
            if def_el:
                lines.append(f"\n*{get_text(def_el)}*\n")
            lines.append("\n---\n")
        return lines

    # ── Infobox ──────────────────────────────────────────────
    if has_class(el, "infobox"):
        if "tip" in classes:
            kind = "tip"
        elif "warn" in classes:
            kind = "warning"
        else:
            kind = "info"
        text = convert_inline(el).strip()
        lines.append(f"\n!!! {kind}\n")
        for line in text.splitlines():
            lines.append(f"    {line}\n")
        lines.append("\n")
        return lines

    # ── Accent box ───────────────────────────────────────────
    if has_class(el, "accent-box"):
        text = convert_inline(el).strip()
        lines.append(f"\n!!! note\n")
        for line in text.splitlines():
            lines.append(f"    {line}\n")
        lines.append("\n")
        return lines

    # ── Subsection ───────────────────────────────────────────
    if has_class(el, "subsection"):
        title_el = el.find(class_="subsection-title")
        if title_el:
            lines.append(f"\n### {get_text(title_el)}\n")
        for child in el.children:
            if isinstance(child, Tag) and not has_class(child, "subsection-title"):
                lines.extend(convert_element(child, depth+1))
        return lines

    # ── Card grid ────────────────────────────────────────────
    if has_class(el, "card-grid"):
        lines.append('\n<div class="grid cards" markdown>\n')
        for card in el.find_all(class_="card", recursive=False):
            h = card.find(["h4","h3","h2"])
            title = get_text(h) if h else ""
            # Get paragraph text
            paras = card.find_all("p")
            desc = " ".join(convert_inline(p).strip() for p in paras)
            lines.append(f"\n-   **{title}**\n\n    {desc}\n")
        lines.append("\n</div>\n")
        return lines

    # ── Node card ────────────────────────────────────────────
    if has_class(el, "node-card"):
        badge_el = el.find(class_="node-badge")
        info_el  = el.find(class_="node-info")
        badge    = get_text(badge_el) if badge_el else ""
        if info_el:
            h = info_el.find(["h4","h3"])
            title = get_text(h) if h else ""
            paras = info_el.find_all("p")
            desc  = " ".join(convert_inline(p).strip() for p in paras)
            lines.append(f"\n**{title}** `{badge}`\n\n{desc}\n\n---\n")
        return lines

    # ── enum-list ────────────────────────────────────────────
    if has_class(el, "enum-list"):
        for li in el.find_all("li"):
            lines.append(f"- {convert_inline(li).strip()}\n")
        lines.append("\n")
        return lines

    # ── Standard block elements ──────────────────────────────
    if tag == "ul":
        for li in el.find_all("li", recursive=False):
            lines.append(f"- {convert_inline(li).strip()}\n")
        lines.append("\n")
        return lines

    if tag == "ol":
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            lines.append(f"{i}. {convert_inline(li).strip()}\n")
        lines.append("\n")
        return lines

    if tag == "p":
        text = convert_inline(el).strip()
        if text:
            lines.append(f"\n{text}\n")
        return lines

    if tag in ("h1","h2","h3","h4","h5"):
        level = int(tag[1])
        lines.append(f"\n{'#' * level} {convert_inline(el).strip()}\n")
        return lines

    if tag == "hr":
        lines.append("\n---\n")
        return lines

    if tag == "pre" or tag == "code":
        lines.append(f"\n```\n{el.get_text()}\n```\n")
        return lines

    if tag == "table":
        rows = el.find_all("tr")
        if not rows:
            return lines
        md_rows = []
        for row in rows:
            cells = row.find_all(["th","td"])
            md_rows.append("| " + " | ".join(convert_inline(c).strip() for c in cells) + " |")
        if md_rows:
            lines.append("\n" + md_rows[0] + "\n")
            # header separator
            col_count = len(rows[0].find_all(["th","td"]))
            lines.append("| " + " | ".join(["---"] * col_count) + " |\n")
            for row in md_rows[1:]:
                lines.append(row + "\n")
        lines.append("\n")
        return lines

    # ── Spacers (skip) ───────────────────────────────────────
    if has_class(el, "spacer") or has_class(el, "spacer-sm") or has_class(el, "footer"):
        return lines

    # ── Default: recurse into children ───────────────────────
    for child in el.children:
        lines.extend(convert_element(child, depth+1))

    return lines


def convert_section(section_el):
    """Convert a section div (with id) to Markdown."""
    lines = []
    section_id = section_el.get("id", "")

    # Section wrapper div — process children
    for child in section_el.children:
        lines.extend(convert_element(child))

    return "".join(lines)


def main():
    print(f"Reading {HTML_SRC} ...")
    with open(HTML_SRC, encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Collect all sections by id
    all_ids = []
    for page_ids in PAGE_MAP.values():
        all_ids.extend(page_ids)

    sections = {}
    for sid in all_ids:
        el = soup.find(id=sid)
        if el:
            sections[sid] = el
        else:
            print(f"  WARNING: section #{sid} not found in HTML")

    os.makedirs(OUT_DIR, exist_ok=True)

    for filename, ids in PAGE_MAP.items():
        out_path = os.path.join(OUT_DIR, filename)
        parts = []
        for sid in ids:
            if sid in sections:
                md = convert_section(sections[sid])
                parts.append(md)
            else:
                parts.append(f"\n<!-- section #{sid} not found -->\n")

        content = "\n".join(parts)
        # Clean up: collapse 3+ blank lines to 2
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip() + "\n"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Wrote {filename} ({len(content)} chars)")

    print("\nDone! Check docs/ folder.")

if __name__ == "__main__":
    main()

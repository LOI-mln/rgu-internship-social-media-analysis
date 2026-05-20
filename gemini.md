# Gemini Agent Instructions - Developer Rules of Engagement

> [!IMPORTANT]
> **Instructions for the AI Assistant**: Read and internalize these guidelines before every turn, response, and code edit in this repository. These rules are absolute constraints and define the specific methodology, style, and engineering standards for Milan Loi's RGU Internship project.

---

## 1. Core Behavioral Constraints

*   **ZERO Emoji Policy (Critical)**:
    *   Do **NOT** use, output, or generate any literal emojis or pictorial icon indicators (e.g., chart, lightbulb, fire, graph, alert, compass, siren symbols) in conversation logs, Streamlit UI codebase, markdown artifacts (`task.md`, `walkthrough.md`, `implementation_plan.md`), or documentation files.
    *   This is an absolute ban. All notifications, headers, info boxes, and text descriptions must be completely emoji-free.
*   **Academic English Standard**:
    *   All user-facing UI text, graph labels, captions, tables, and interpretation texts must be written in professional, rigorous, university-level academic English suitable for evaluation by Robert Gordon University (RGU).
    *   Avoid colloquialisms, marketing jargon, or casual tones.

---

## 2. Dashboard UI & Design System Rules (Sober & Flat)

Do **NOT** implement modern, flashy, or glossy web app widgets. Keep the layout flat, formal, and documentation-like.

*   **Sober Sidebar Navigation**:
    *   Do **NOT** style sidebar links as button cards, rounded boxes, container items, or checkable boxes.
    *   Keep the sidebar menu styled as a flat vertical list of plain text options.
    *   **Selected Option Style**: Make the active text bold (`font-weight: 700`), colored in professional blue (`#3B82F6`), and prepended with a classic text arrow `> ` (e.g., `> 3. Polarization & Toxicity`). Do **NOT** apply any background colors, borders, or shadows to the active container.
    *   **Hover Style**: Only change the text color to solid white (`#FFFFFF`) on hover, keeping the background completely transparent (`background-color: transparent`). Do **NOT** use translation lifts (`translateY`), shadows, or borders.
    *   **Hide Radio Circles**: Ensure all Streamlit radio circles and dots are hidden via CSS selectors (`[role="presentation"]` and `StyledRadio`).
*   **Professional Sapphire Blue Palette**:
    *   Do **NOT** use bright, neon, or flashing red/pink colors (`#FF4B2B` or `#FF416C`) for text elements, active states, or separators.
    *   Style all major headers (`h1`, `h2`, `h3`) and horizontal line dividers (`hr`) using a professional sapphire-to-royal-blue gradient (`#3B82F6` to `#1D4ED8`).
*   **No Logos**:
    *   Do **NOT** load or display any logo images in the sidebar. Keep the top of the sidebar clean, functional, and purely text-oriented.

---

## 3. Data Representation & Normalization Philosophy

*   **Relative Column-Wise Normalization (Heatmaps)**:
    *   When plotting metrics such as toxicity or polarization that reside in compressed, non-reaching absolute ranges (e.g., observed mean toxicity values range between `0.38` and `0.52`), always apply individual column-level min-max normalization to stretch the color contrasts from green to red. This prevents the flattening effect where all groups appear "nice" (yellow/green).
*   **No Absolute Color Scales**:
    *   Always hide the continuous color scale/legend bar (`coloraxis_showscale=False`) from the heatmap UI. A generic `0.0` to `1.0` scale is misleading since actual toxicity never reaches `1.0`.
    *   **Always Overlay Raw Values**: Write/annotate the exact, absolute numeric values (e.g., `0.38`, `0.52`) directly inside the heatmap cells and within interactive hover tooltips so the raw metrics remain completely transparent to the user.

---

## 4. Spacing & Layout Structure

*   **Full-Width Vertical Stack**:
    *   Do **NOT** compress visual elements (like heatmaps and dataframes) into side-by-side columns.
    *   Always stack major analytical widgets vertically at full-width (`use_container_width=True`) to maximize visibility and spacing on all screen resolutions.
    *   Provide scholarly, interpretative guidelines immediately underneath both the heatmap and the table components.

---

## 5. Resource Autonomy

*   **Zero External Dependencies for Assets**:
    *   Never hotlink or load user interface icons, logos, or backgrounds from external URLs. Use plain text styles or purely local assets to ensure complete offline reliability.

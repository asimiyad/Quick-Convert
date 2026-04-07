# Design System Strategy: Kinetic Noir

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The High-Performance Engine."** 

We are moving away from the "utility-tool" aesthetic and toward a "precision-instrument" experience. Most conversion tools feel cluttered and secondary; this system treats the file conversion process as a high-stakes, cinematic event. By utilizing a deep `#000000` base and piercing `#FF0000` accents, we evoke the feeling of a high-end sports car dashboard or a premium dark-mode editing suite.

To break the "template" look, we embrace **intentional asymmetry**—placing heavy typography on the left and allowing generous negative space on the right. We avoid rigid grids in favor of overlapping elements where file "cards" may slightly bleed over container boundaries to suggest speed and fluidity.

---

### 2. Colors: Tonal Depth & "No-Line" Philosophy
The color palette is built on the contrast between absolute void and kinetic energy.

*   **The "No-Line" Rule:** Visual separation is never achieved through 1px solid borders. Use the `surface-container` hierarchy. To separate a conversion queue from the main dashboard, place a `surface-container-low` (#131313) panel against the `background` (#0e0e0e). The transition is felt, not seen.
*   **Surface Hierarchy:** 
    *   **Level 0 (Base):** `surface` (#0e0e0e) for the global canvas.
    *   **Level 1 (Sections):** `surface-container-low` (#131313) for secondary sidebars.
    *   **Level 2 (Active Areas):** `surface-container-high` (#1f1f1f) for main interaction zones (e.g., the drop zone).
*   **The "Glass & Gradient" Rule:** Primary CTAs should not be flat. Use a subtle linear gradient from `primary` (#ff8e7d) to `primary_dim` (#eb0000) at a 135-degree angle. This adds a "backlit" quality to the red accents. For floating overlays, use `surface_container_highest` at 70% opacity with a `24px` backdrop-blur.

---

### 3. Typography: The Editorial Impact
We use **Inter** as our typographic backbone, but we treat it with editorial intent.

*   **Display Scales:** Use `display-lg` (3.5rem) with `-0.04em` letter spacing for hero headers. This "tight" tracking creates a compressed, high-velocity look.
*   **The Contrast Play:** Pair `headline-lg` (2rem) in white (`on_surface`) with `label-md` (0.75rem) in `on_surface_variant` (#ababab) set in all-caps with `0.1em` letter spacing. This creates a sophisticated "Pro-Tools" hierarchy.
*   **Functional Clarity:** All body text (`body-md`) must remain white on dark surfaces to maintain a 12.5:1 contrast ratio, ensuring the tool is usable in low-light professional environments.

---

### 4. Elevation & Depth: Tonal Stacking
Forget shadows that look like "drops." We define depth through **Tonal Layering.**

*   **The Layering Principle:** To lift a file-status card, place it on a `surface-container-lowest` (#000000) background if the surrounding section is `surface-container-low`. The change in "blackness" creates a natural recessed or protruding effect.
*   **Ambient Shadows:** If a modal requires a shadow, use a 40px blur with only 6% opacity, tinted with `primary_dim` (#eb0000). This creates a subtle "red glow" rather than a grey smudge, suggesting the element is powered by the system's energy.
*   **Ghost Borders:** For inactive states or secondary drop zones, use `outline_variant` (#484848) at 15% opacity. It should be a mere whisper of a boundary.

---

### 5. Components: Precision Primitives

*   **The Kinetic Button (Primary):** 
    *   **Background:** Gradient of `primary_fixed` to `primary_dim`.
    *   **Radius:** `full` (pill-shaped) to represent speed.
    *   **Interaction:** On hover, increase the `primary_container` glow.
*   **The Drop Zone (Card):** 
    *   **Background:** `surface_container_low`.
    *   **Radius:** `xl` (1.5rem). 
    *   **Constraint:** No dividers. Use `32px` of internal padding to let the "File Icon" and "File Name" breathe.
*   **Status Chips:** 
    *   Use `secondary_container` for "Processing" and `tertiary_container` for "Complete."
    *   Keep background opacity at 20% but keep the text at 100% for a "neon" effect.
*   **Input Fields:** 
    *   No bottom line or box border. Use a `surface_container_highest` fill with a `sm` (0.25rem) radius.
    *   Active state: A `1px` "Ghost Border" using `primary` at 40% opacity.
*   **Conversion Progress Bar:** 
    *   **Track:** `surface_variant`. 
    *   **Indicator:** `primary` (#ff8e7d). 
    *   **Detail:** Add a subtle outer glow to the leading edge of the progress bar to simulate a "spark" of data movement.

---

### 6. Do's and Don'ts

#### Do:
*   **Do** use extreme white space. A high-performance tool shouldn't feel "cramped."
*   **Do** use `primary` red sparingly. It is a laser, not a paint bucket. Use it only for the "Convert" trigger and critical errors.
*   **Do** animate transitions. Elements should "slide" into place with a `cubic-bezier(0.16, 1, 0.3, 1)` easing curve (the "Power Out" curve).

#### Don't:
*   **Don't** use pure grey (#808080). Use the `on_surface_variant` (#ababab) to keep the dark theme feeling "expensive."
*   **Don't** use 1px dividers to separate list items. Use an `8px` vertical gap.
*   **Don't** use standard "Information Blue." Use `tertiary` (purples/violets) for non-critical info to keep the "Noir" palette consistent.
---
name: paper-plot-skill
description: Apply the Plotbar warm-pastel Matplotlib template to create or restyle Python publication figures with consistent axes, panel labels, heatmaps, and editable vector export. Use when the user asks for the Plotbar template or this specific visual style; do not route R/ggplot-only or unrelated plotting-style requests here.
---

# Paper Plot Skill

Create a clear, publication-ready figure while preserving the user's data, calculations, labels, and intended message. The bundled Python module is the source of truth for colors, typography, axes, annotations, and export behavior.

## Workflow

1. Inspect the data and any existing plotting code. Identify the comparison the figure must communicate, the final physical size, and the requested formats. Infer sensible defaults when these are not specified.
2. Read [references/style-contract.md](references/style-contract.md) before designing, restyling, or reviewing a figure. It defines the palette roles, supported helpers, and layout constraints.
3. Reuse [assets/plotbar](assets/plotbar) rather than reimplementing its constants or helpers:
   - If the target project already has a `plotbar` module, inspect it and use it when compatible.
   - For durable project code, copy the bundled package into an appropriate project source directory and import from that project-local copy.
   - For a one-off render, add this skill's `assets` directory to `sys.path` at runtime. Do not leave a machine-specific skill path in code delivered to the user.
   - Never overwrite an existing project module without inspecting the overlap first.
4. Call `apply_publication_style()` before creating the figure, set an explicit `figsize`, and call `style_axes()` for every ordinary plot axis. Use the bundled palette and colormaps; preserve consistent color meaning across panels.
5. Render a PNG preview at the final aspect ratio and inspect it visually. Correct clipping, overlap, weak contrast, ambiguous legends, dense ticks, and unreadable annotations. Do not accept a figure solely because the script ran.
6. Export with `save_publication_figure()`. Default to editable PDF when the user does not specify a format; add SVG or PNG only when useful or requested.

## Invariants

- Styling must not alter values, statistical results, category order, uncertainty, or sample-size meaning.
- Keep typography readable at final size. Reduce content or revise layout before shrinking important text below the template's small-font constants.
- Use panel labels for multi-panel figures and keep axes, labels, legends, and annotations aligned across panels.
- Preserve vector text and geometry for PDF/SVG. Do not rasterize the complete figure just to simplify export.
- Treat `finite_or_zero()` as an explicit rendering utility, not an analytical missing-data policy. Never silently replace invalid observations in calculations.
- Use color redundantly with line style, marker, position, or direct labels when grayscale reproduction or accessibility matters.

## Resources

- [references/style-contract.md](references/style-contract.md): read for visual design, API selection, and review criteria.
- [assets/plotbar](assets/plotbar): reusable Python package containing the authoritative template.
- `scripts/render_style_preview.py`: run as a smoke test or inspect as a compact usage example. It writes both PDF and PNG outputs.

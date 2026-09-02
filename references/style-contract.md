# Plotbar style contract

## Visual signature

Plotbar uses a warm, low-saturation pastel system on white with dark brown-gray ink. It favors light dotted grids, left/bottom spines, compact sans-serif typography, restrained line weights, and editable vector output. The style should feel quiet and precise rather than decorative.

The authoritative palette order is:

| Index | Hex | Typical role |
| ---: | --- | --- |
| 0 | `#F2E3B2` | pale baseline or first series |
| 1 | `#F9DCA4` | warm secondary series |
| 2 | `#FFE3B4` | light highlight |
| 3 | `#F6C8A7` | peach comparison |
| 4 | `#E0A48E` | strongest warm emphasis |
| 5 | `#D2B6B1` | muted mauve-neutral |
| 6 | `#D4C7B4` | stone neutral |
| 7 | `#E3B3B5` | muted rose / diverging low end |
| 8 | `#D0E3D1` | muted green / diverging high end |

Use `INK`, `MID_INK`, `GRID`, and `WHITE` for structural elements. When a pastel needs more contrast, derive a same-hue darker edge with `blend(color, target=INK, fraction=...)`; do not introduce arbitrary saturated colors.

## Public API

Import public names from `plotbar`, not from `plotbar.style`.

| Helper | Use |
| --- | --- |
| `apply_publication_style()` | Set fonts, vector-font export, axes, grid, legend, and save defaults before creating figures. |
| `style_axes(ax, grid_axis=..., zero_line=...)` | Normalize spines, ticks, grids, and optional zero reference for each ordinary axis. |
| `add_panel_label(ax, "A")` | Place bold panel letters in axes coordinates. Adjust `x`/`y` only for layout. |
| `add_line_outline(line)` | Improve contrast of a pastel data line while retaining its hue. Use on important lines, not every decorative mark. |
| `pastel_diverging_cmap()` | Heatmaps with a meaningful central reference and two directions. Set a symmetric or otherwise meaningful normalization explicitly. |
| `pastel_sequential_cmap()` | Ordered nonnegative or monotonic heatmap values. |
| `annotate_heatmap(ax, values, ...)` | Add compact cell labels; suppress or simplify them when cells are too small. |
| `save_publication_figure(fig, output_dir, stem, formats=...)` | Export tight PDF/SVG/PNG and close the figure. PDF is the default. |
| `finite_or_zero(values)` | Convert non-finite values to zero only when zero is explicitly the desired drawing fallback. |

Reusable constants include `PALETTE`, `INK`, `MID_INK`, `GRID`, `WHITE`, `LINE_WIDTH`, `MARKER_EDGE_WIDTH`, `AXIS_LINE_WIDTH`, `TICK_LINE_WIDTH`, `DEFAULT_FONT_SIZE`, `SMALL_FONT_SIZE`, and `DENSE_TICK_FONT_SIZE`.

## Mark-specific guidance

### Lines and points

- Give the main series the clearest position and a darker outline when needed.
- For overlapping series, combine color with marker shape or line style.
- Use direct labels when a legend would force unnecessary eye travel.
- Do not connect observations when the implied continuity is false.

### Bars

- Start quantitative bar axes at zero unless a justified alternative is visibly disclosed.
- Use a darker same-hue edge derived with `blend()` and `MARKER_EDGE_WIDTH`.
- Keep category order analytically meaningful. Do not reorder categories merely for visual symmetry.

### Heatmaps

- Choose sequential versus diverging color by the meaning of the scale, not aesthetics.
- For diverging values, center the normalization on the true reference value, commonly zero.
- Keep cell text compact and remove it if it becomes illegible; a readable colorbar is preferable to crowded annotations.

### Multi-panel figures

- Use explicit physical dimensions and a layout engine such as `constrained_layout` when compatible.
- Share axes only when scales and meaning genuinely match.
- Label panels `A`, `B`, `C`, ... in reading order with `add_panel_label()`.
- Keep repeated legends and labels to a minimum without sacrificing interpretation.

## Minimal starter

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotbar import (
    PALETTE,
    add_line_outline,
    apply_publication_style,
    save_publication_figure,
    style_axes,
)

apply_publication_style()
x = np.arange(6)
y = np.array([1.2, 1.6, 1.5, 2.1, 2.4, 2.8])

fig, ax = plt.subplots(figsize=(3.35, 2.35), constrained_layout=True)
line, = ax.plot(x, y, marker="o", color=PALETTE[4], label="Observed")
add_line_outline(line)
style_axes(ax, grid_axis="y")
ax.set(xlabel="Time", ylabel="Response")
ax.legend()

save_publication_figure(fig, Path("figures"), "response", formats=("pdf", "png"))
```

## Review checklist

- The intended comparison is obvious before reading the caption.
- Axes include units where relevant, and category/tick labels are unambiguous.
- Color meaning is consistent and still recoverable without color alone when necessary.
- No text, marker, error bar, panel label, or legend is clipped.
- Grid and outlines support the data rather than competing with it.
- Font size and line weight are judged at final physical size, not only in a zoomed preview.
- Vector output opens correctly, retains selectable text where the format supports it, and matches the PNG preview.

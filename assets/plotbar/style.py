"""Reusable publication-figure styling and vector-safe export helpers."""

from __future__ import annotations

from itertools import count
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


PALETTE = [
    "#F2E3B2",
    "#F9DCA4",
    "#FFE3B4",
    "#F6C8A7",
    "#E0A48E",
    "#D2B6B1",
    "#D4C7B4",
    "#E3B3B5",
    "#D0E3D1",
]

INK = "#3E3A38"
MID_INK = "#77716D"
GRID = "#D8D3CE"
WHITE = "#FFFFFF"
LINE_WIDTH = 1.20
MARKER_EDGE_WIDTH = 0.60
AXIS_LINE_WIDTH = 0.85
TICK_LINE_WIDTH = 0.75
LINE_OUTLINE_EXTRA_WIDTH = 0.65
DEFAULT_FONT_SIZE = 8.4
SMALL_FONT_SIZE = 7.0
DENSE_TICK_FONT_SIZE = 7.3
_OUTLINED_LINE_IDS = count()


def blend(color: str, target: str = INK, fraction: float = 0.22) -> str:
    rgb = np.asarray(mcolors.to_rgb(color))
    target_rgb = np.asarray(mcolors.to_rgb(target))
    return mcolors.to_hex((1.0 - fraction) * rgb + fraction * target_rgb)


def add_line_outline(
    line: Line2D,
    *,
    extra_width: float = LINE_OUTLINE_EXTRA_WIDTH,
    darkness: float = 0.48,
) -> Line2D:
    """Add a darker same-hue outline to a plotted data line."""

    outline = blend(line.get_color(), target=INK, fraction=darkness)
    line.set_gid(f"outlined_data_line_{next(_OUTLINED_LINE_IDS)}")
    line.set_path_effects(
        [
            path_effects.Stroke(linewidth=line.get_linewidth() + extra_width, foreground=outline),
            path_effects.Normal(),
        ]
    )
    return line


def apply_publication_style(base_font_size: float = DEFAULT_FONT_SIZE) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.size": base_font_size,
            "axes.titlesize": base_font_size + 0.5,
            "axes.labelsize": base_font_size,
            "axes.titleweight": "bold",
            "axes.edgecolor": INK,
            "axes.linewidth": AXIS_LINE_WIDTH,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.55,
            "grid.linestyle": ":",
            "grid.alpha": 0.75,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "xtick.major.width": TICK_LINE_WIDTH,
            "ytick.major.width": TICK_LINE_WIDTH,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "axes.labelcolor": INK,
            "legend.frameon": False,
            "legend.fontsize": base_font_size - 0.3,
            "lines.linewidth": LINE_WIDTH,
            "lines.markersize": 4.5,
            "errorbar.capsize": 2.5,
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "savefig.facecolor": WHITE,
            "savefig.transparent": False,
        }
    )


def style_axes(ax: plt.Axes, *, grid_axis: str = "both", zero_line: bool = False) -> plt.Axes:
    for side, spine in ax.spines.items():
        spine.set_visible(side in {"left", "bottom"})
        spine.set_color(INK)
        spine.set_linewidth(AXIS_LINE_WIDTH)
    ax.tick_params(which="both", top=False, right=False, pad=2.0, width=TICK_LINE_WIDTH)
    ax.grid(True, axis=grid_axis, color=GRID, linestyle=":", linewidth=0.55, alpha=0.75)
    if zero_line:
        ax.axhline(0, color=MID_INK, linewidth=0.8, zorder=1)
    return ax


def add_panel_label(
    ax: plt.Axes,
    label: str,
    *,
    x: float = -0.12,
    y: float = 1.06,
    fontsize: float = 9.0,
) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=fontsize,
        fontweight="bold",
        color=INK,
        clip_on=False,
    )


def pastel_diverging_cmap() -> mcolors.LinearSegmentedColormap:
    return mcolors.LinearSegmentedColormap.from_list(
        "plotbar_diverging",
        [blend(PALETTE[7], fraction=0.12), WHITE, blend(PALETTE[8], fraction=0.12)],
    )


def pastel_sequential_cmap() -> mcolors.LinearSegmentedColormap:
    return mcolors.LinearSegmentedColormap.from_list(
        "plotbar_sequential",
        [WHITE, PALETTE[0], PALETTE[3], blend(PALETTE[4], fraction=0.08)],
    )


def annotate_heatmap(
    ax: plt.Axes,
    values: np.ndarray,
    *,
    fmt: str = ".2f",
    labels: np.ndarray | None = None,
    fontsize: float = SMALL_FONT_SIZE,
) -> None:
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = values[i, j]
            if not np.isfinite(value):
                text = "—"
            elif labels is not None:
                text = str(labels[i, j])
            else:
                text = format(value, fmt)
            ax.text(j, i, text, ha="center", va="center", fontsize=fontsize, color=INK)


def save_publication_figure(
    fig: plt.Figure,
    output_dir: Path,
    stem: str,
    *,
    formats: Sequence[str] = ("pdf",),
    dpi: int = 360,
    pad_inches: float = 0.04,
) -> list[Path]:
    """Save a figure, defaulting to an editable vector PDF.

    ``formats`` may contain ``pdf``, ``svg``, or ``png``. PDF and SVG retain
    vector geometry; PDF text is embedded as TrueType through the package
    style configuration.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    metadata = {"Creator": "Python/matplotlib", "Title": stem}
    normalized = tuple(dict.fromkeys(item.lower().lstrip(".") for item in formats))
    unsupported = sorted(set(normalized) - {"pdf", "svg", "png"})
    if unsupported:
        raise ValueError("Unsupported output format(s): " + ", ".join(unsupported))
    if not normalized:
        raise ValueError("At least one output format is required")
    for suffix in normalized:
        out = output_dir / f"{stem}.{suffix}"
        save_options = {
            "format": suffix,
            "bbox_inches": "tight",
            "pad_inches": pad_inches,
            "metadata": metadata,
        }
        if suffix == "png":
            save_options["dpi"] = dpi
        fig.savefig(out, **save_options)
        paths.append(out)
    plt.close(fig)
    return paths


def finite_or_zero(values: Iterable[float]) -> np.ndarray:
    out = np.asarray(list(values), dtype=float)
    out[~np.isfinite(out)] = 0.0
    return out

#!/usr/bin/env python3
"""Render a compact Plotbar style preview and smoke-test the bundled API."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "assets"))

from plotbar import (  # noqa: E402
    INK,
    MARKER_EDGE_WIDTH,
    PALETTE,
    add_line_outline,
    add_panel_label,
    annotate_heatmap,
    apply_publication_style,
    blend,
    pastel_diverging_cmap,
    save_publication_figure,
    style_axes,
)


def build_preview() -> plt.Figure:
    apply_publication_style()
    fig, axes = plt.subplots(1, 3, figsize=(8.2, 2.45), constrained_layout=True)

    x = np.arange(1, 7)
    for index, (label, values, marker) in enumerate(
        [
            ("Reference", [1.0, 1.3, 1.5, 1.7, 2.0, 2.2], "o"),
            ("Treatment", [1.1, 1.4, 1.8, 2.1, 2.6, 3.0], "s"),
        ]
    ):
        color = PALETTE[4 + index]
        line, = axes[0].plot(x, values, marker=marker, color=color, label=label)
        add_line_outline(line)
    style_axes(axes[0], grid_axis="y")
    axes[0].set(xlabel="Time", ylabel="Response", title="Trend")
    axes[0].legend(loc="upper left")

    categories = ["A", "B", "C", "D"]
    values = np.array([2.4, 3.1, 2.8, 3.6])
    colors = PALETTE[:4]
    axes[1].bar(
        categories,
        values,
        color=colors,
        edgecolor=[blend(color, fraction=0.42) for color in colors],
        linewidth=MARKER_EDGE_WIDTH,
    )
    style_axes(axes[1], grid_axis="y")
    axes[1].set(ylabel="Estimate", title="Categories")

    matrix = np.array([[-0.8, -0.3, 0.2], [-0.2, 0.0, 0.5], [0.3, 0.7, 1.0]])
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    image = axes[2].imshow(matrix, cmap=pastel_diverging_cmap(), norm=norm)
    annotate_heatmap(axes[2], matrix, fmt=".1f")
    axes[2].set(
        xticks=range(3),
        yticks=range(3),
        xticklabels=["X", "Y", "Z"],
        yticklabels=["Low", "Mid", "High"],
        title="Diverging values",
    )
    axes[2].grid(False)
    for spine in axes[2].spines.values():
        spine.set_visible(False)
    colorbar = fig.colorbar(image, ax=axes[2], fraction=0.05, pad=0.04)
    colorbar.outline.set_edgecolor(INK)
    colorbar.outline.set_linewidth(0.6)

    for label, ax in zip("ABC", axes):
        add_panel_label(ax, label)
    return fig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SKILL_DIR / "preview",
        help="Directory for plotbar-style-preview.pdf and .png",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = save_publication_figure(
        build_preview(),
        args.output_dir,
        "plotbar-style-preview",
        formats=("pdf", "png"),
    )
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()

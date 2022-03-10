from __future__ import annotations

import math
from typing import Any

import numpy as np
import plotext as plt
import rich.align
import rich.box
import rich.console
import rich.panel
import rich.pretty
import rich.text
import textual.widget
import uproot

import uproot_browser.dirs
import uproot_browser.plot

EMPTY = object()


def make_plot(item: Any, *size: int) -> Any:
    plt.clf()
    plt.plotsize(*size)
    h_item = uproot_browser.plot.plot(item)
    inner_sum = np.sum(h_item.values())
    full_sum = np.sum(h_item.values(flow=True))
    if math.isclose(inner_sum, full_sum):
        plt.title(f"{item.name} - Entries = {inner_sum:g}")
    else:
        plt.title(f"{item.name} - Entries = {inner_sum:g} ({full_sum:g} with flow)")
    plt.xlabel(f"{h_item.axes[0].name}")
    return plt.build()


class Plot:
    def __init__(self, item: Any) -> None:
        self.item: Any = item

    def __rich_console__(
        self, console: rich.console.Console, options: rich.console.ConsoleOptions
    ) -> rich.console.RenderResult:
        width = options.max_width or console.width
        height = options.height or console.height
        try:
            canvas = make_plot(self.item, width, height)
            yield rich.text.Text.from_ansi(canvas)
        except Exception:
            tb = rich.traceback.Traceback(
                extra_lines=1,
                max_frames=4,  # Can't be less than 4 frames
            )
            tb.max_frames = 2
            yield tb


class PlotWidget(textual.widget.Widget):
    def __init__(self, uproot_file: uproot.ReadOnlyFile) -> None:
        super().__init__()
        self.file = uproot_file
        self.plot = EMPTY

    def set_plot(self, plot_path: str | None) -> None:
        if plot_path is None:
            self.plot = plot_path
        else:
            *_, item = uproot_browser.dirs.apply_selection(
                self.file, plot_path.split(":")
            )
            self.plot = Plot(item)

    async def update(self) -> None:
        self.refresh()

    def render(self) -> rich.console.RenderableType:
        if self.plot is None:
            return rich.panel.Panel(
                rich.align.Align.center(
                    rich.pretty.Pretty(
                        "No plot selected!", no_wrap=True, overflow="ellipsis"
                    ),
                    vertical="middle",
                ),
                border_style="red",
                box=rich.box.ROUNDED,
            )

        if self.plot is EMPTY:
            return rich.panel.Panel(
                rich.align.Align.center(
                    rich.text.Text.from_ansi(
                        """
┬ ┬┌─┐┬─┐┌─┐┌─┐┌┬┐4 ┌┐ ┬─┐┌─┐┬ ┬┌─┐┌─┐┬─┐
│ │├─┘├┬┘│ ││ │ │───├┴┐├┬┘│ ││││└─┐├┤ ├┬┘
└─┘┴  ┴└─└─┘└─┘ ┴   └─┘┴└─└─┘└┴┘└─┘└─┘┴└─
                          powered by Hist""",
                        no_wrap=True,
                    ),
                    vertical="middle",
                ),
                border_style="green",
                box=rich.box.ROUNDED,
            )

        return rich.panel.Panel(self.plot)  # type: ignore[arg-type]

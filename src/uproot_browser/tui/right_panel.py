from __future__ import annotations

import dataclasses
from typing import Any

import numpy as np
import plotext as plt  # plots in text
import rich.panel
import rich.text
import rich.traceback
import textual.widget
import textual.widgets

import uproot_browser.plot

LOGO = """\
Scikit-HEP
┬ ┬┌─┐┬─┐┌─┐┌─┐┌┬┐5 ┌┐ ┬─┐┌─┐┬ ┬┌─┐┌─┐┬─┐
│ │├─┘├┬┘│ ││ │ │───├┴┐├┬┘│ ││││└─┐├┤ ├┬┘
└─┘┴  ┴└─└─┘└─┘ ┴   └─┘┴└─└─┘└┴┘└─┘└─┘┴└─
                Powered by Textual & Hist"""

LOGO_PANEL = rich.text.Text.from_ansi(LOGO, no_wrap=True)


placeholder = np.random.rand(1000)


def make_plot(item: Any, theme: str, *size: int) -> Any:
    plt.clf()
    plt.plotsize(*size)
    uproot_browser.plot.plot(item)
    plt.theme(theme)
    return plt.build()


# wrapper for plotext into a textual widget
@dataclasses.dataclass
class Plotext:
    item: Any
    theme: str

    def __rich_console__(self, console, options):
        if self.item is None:
            yield rich.text.Text()
            return
        width = options.max_width or console.width
        height = options.height or console.height

        canvas = make_plot(self.item, self.theme, width, height)
        yield rich.text.Text.from_ansi(canvas)


class PlotWidget(textual.widget.Widget):
    _item: Plotext

    @property
    def item(self) -> Plotext:
        return self._item

    @item.setter
    def item(self, value: Plotext) -> None:
        self._item = value
        self.refresh()

    def __init__(self, uproot_item=None, **kargs):
        super().__init__(**kargs)
        self._item = None

    def render(self) -> rich.console.RenderableType:
        return self.item


class EmptyWidget(textual.widget.Widget):
    # if the plot is empty

    def render(self) -> rich.console.RenderableType:
        return rich.text.Text("Plot is Empty")


class LogoWidget(textual.widget.Widget):
    def render(self) -> rich.console.RenderableType:
        return LOGO_PANEL


@dataclasses.dataclass
class Error:
    exc: tuple

    def __rich_console__(
        self, console: rich.console.Console, options: rich.console.ConsoleOptions
    ) -> rich.console.RenderResult:
        width = options.max_width or console.width

        yield rich.traceback.Traceback.from_exception(*self.exc, width=width)


class ErrorWidget(textual.widgets.TextLog):
    _exc: Error

    @property
    def exc(self) -> Error:
        return self._exc

    @exc.setter
    def exc(self, value: tuple) -> None:
        self._exc = Error(value)
        self.clear()
        self.write(self._exc)
        # self.refresh()

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.write("No Exception set!")
        self._exc = None

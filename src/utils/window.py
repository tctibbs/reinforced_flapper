"""Module containing the game window class."""


class Window:
    """Game window.

    Attributes:
        width: Window width.
        height: Window height.
        ratio: Window aspect ratio.
        w: Window width.
        h: Window height.
        r: Window aspect ratio.
        viewport_width: Viewport width.
        viewport_height: Viewport height.
        vw: Viewport width.
        vh: Viewport height.
        vr: Viewport
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.ratio = width / height
        self.w = width
        self.h = height
        self.r = width / height
        self.viewport_width = width
        self.viewport_height = height * 0.79
        self.vw = width
        self.vh = height * 0.79
        self.viewport_ratio = self.vw / self.vh
        self.vr = self.vw / self.vh

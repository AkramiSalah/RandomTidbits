"""
terminal_display
----------------
A minimal terminal rendering library for text-based frames.
"""

from .frame import Frame
from .renderer import Renderer
from .display import Display

__all__ = ["Frame", "Renderer", "Display"]

__version__ = "0.1.0"
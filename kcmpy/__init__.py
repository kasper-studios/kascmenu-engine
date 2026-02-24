"""Modern CUI Framework for Python."""
from .core.app import App
from .core.component import Component, Rect
from .core.renderer import Renderer, Style
from .core.theme import Theme, Themes, ColorScheme, get_theme, set_theme, apply_theme_to_widget
from .cui.widgets import Box, Text
from .cui.menu import Menu, MenuItem, SelectList
from .cui.progress import ProgressBar, Spinner, MultiProgressBar, StatusIndicator
from .cui.input import TextInput, Checkbox, RadioGroup, Button
from .events.event_system import EventBus, Event, EventType

__version__ = "0.1.0"
__all__ = [
    'App', 'Component', 'Rect', 'Renderer', 'Style',
    'Theme', 'Themes', 'ColorScheme', 'get_theme', 'set_theme', 'apply_theme_to_widget',
    'Box', 'Text', 'Menu', 'MenuItem', 'SelectList',
    'ProgressBar', 'Spinner', 'MultiProgressBar', 'StatusIndicator',
    'TextInput', 'Checkbox', 'RadioGroup', 'Button',
    'EventBus', 'Event', 'EventType'
]

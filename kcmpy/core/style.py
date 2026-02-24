"""Advanced styling system for widgets."""
from dataclasses import dataclass
from typing import Optional, Tuple
import platform


@dataclass
class Padding:
    """Padding configuration."""
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0
    
    @classmethod
    def all(cls, value: int):
        """Create padding with same value on all sides."""
        return cls(value, value, value, value)
    
    @classmethod
    def symmetric(cls, vertical: int = 0, horizontal: int = 0):
        """Create symmetric padding."""
        return cls(vertical, horizontal, vertical, horizontal)


@dataclass
class Border:
    """Border configuration."""
    style: str = 'single'  # single, double, rounded, thick, ascii, none
    color: str = 'white'
    show_top: bool = True
    show_right: bool = True
    show_bottom: bool = True
    show_left: bool = True
    
    # Border character sets
    STYLES = {
        'single': {
            'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
            'h': '─', 'v': '│', 't': '┬', 'b': '┴', 'l': '├', 'r': '┤', 'c': '┼'
        },
        'double': {
            'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
            'h': '═', 'v': '║', 't': '╦', 'b': '╩', 'l': '╠', 'r': '╣', 'c': '╬'
        },
        'rounded': {
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'h': '─', 'v': '│', 't': '┬', 'b': '┴', 'l': '├', 'r': '┤', 'c': '┼'
        },
        'thick': {
            'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛',
            'h': '━', 'v': '┃', 't': '┳', 'b': '┻', 'l': '┣', 'r': '┫', 'c': '╋'
        },
        'ascii': {
            'tl': '+', 'tr': '+', 'bl': '+', 'br': '+',
            'h': '-', 'v': '|', 't': '+', 'b': '+', 'l': '+', 'r': '+', 'c': '+'
        },
        'none': {
            'tl': ' ', 'tr': ' ', 'bl': ' ', 'br': ' ',
            'h': ' ', 'v': ' ', 't': ' ', 'b': ' ', 'l': ' ', 'r': ' ', 'c': ' '
        }
    }
    
    def get_chars(self):
        """Get border characters, using ASCII on Windows if needed."""
        is_windows = platform.system() == 'Windows'
        style = 'ascii' if is_windows and self.style not in ['ascii', 'none'] else self.style
        return self.STYLES.get(style, self.STYLES['single'])


@dataclass
class Shadow:
    """Shadow effect configuration."""
    enabled: bool = False
    offset_x: int = 1
    offset_y: int = 1
    char: str = '░'
    color: str = 'bright_black'


@dataclass
class WidgetStyle:
    """Complete widget styling configuration."""
    # Layout
    padding: Padding = None
    margin: Padding = None
    
    # Border
    border: Border = None
    
    # Visual effects
    shadow: Shadow = None
    
    # Background
    background: Optional[str] = None
    
    # Alignment
    align: str = 'left'  # left, center, right
    valign: str = 'top'  # top, middle, bottom
    
    # Size constraints
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.padding is None:
            self.padding = Padding()
        if self.margin is None:
            self.margin = Padding()
        if self.border is None:
            self.border = Border(style='none')
        if self.shadow is None:
            self.shadow = Shadow()
    
    def get_content_rect(self, outer_rect):
        """Calculate content rectangle after applying padding and border."""
        from ..core.component import Rect
        
        x = outer_rect.x + self.margin.left
        y = outer_rect.y + self.margin.top
        width = outer_rect.width - self.margin.left - self.margin.right
        height = outer_rect.height - self.margin.top - self.margin.bottom
        
        # Account for border
        if self.border.style != 'none':
            if self.border.show_left:
                x += 1
                width -= 1
            if self.border.show_right:
                width -= 1
            if self.border.show_top:
                y += 1
                height -= 1
            if self.border.show_bottom:
                height -= 1
        
        # Account for padding
        x += self.padding.left
        y += self.padding.top
        width -= self.padding.left + self.padding.right
        height -= self.padding.top + self.padding.bottom
        
        return Rect(x, y, max(0, width), max(0, height))


class StyledWidget:
    """Mixin for widgets with advanced styling."""
    
    def __init__(self):
        self.widget_style = WidgetStyle()
    
    def set_style(self, **kwargs):
        """Set style properties."""
        for key, value in kwargs.items():
            if hasattr(self.widget_style, key):
                setattr(self.widget_style, key, value)
    
    def set_padding(self, *args, **kwargs):
        """Set padding. Can be called as:
        - set_padding(10) - all sides
        - set_padding(10, 20) - vertical, horizontal
        - set_padding(top=10, left=5) - specific sides
        """
        if len(args) == 1:
            self.widget_style.padding = Padding.all(args[0])
        elif len(args) == 2:
            self.widget_style.padding = Padding.symmetric(args[0], args[1])
        elif kwargs:
            for key, value in kwargs.items():
                setattr(self.widget_style.padding, key, value)
    
    def set_border(self, style: str = 'single', color: str = 'white', **kwargs):
        """Set border style."""
        self.widget_style.border = Border(style=style, color=color, **kwargs)
    
    def set_shadow(self, enabled: bool = True, offset_x: int = 1, offset_y: int = 1):
        """Enable/configure shadow."""
        self.widget_style.shadow = Shadow(enabled, offset_x, offset_y)
    
    def render_border(self, renderer, rect):
        """Render border around rectangle."""
        if self.widget_style.border.style == 'none':
            return
        
        from ..core.renderer import Style
        
        border = self.widget_style.border
        chars = border.get_chars()
        style = Style(fg=border.color)
        
        # Top border
        if border.show_top:
            renderer.move_cursor(rect.x, rect.y)
            line = chars['tl'] if border.show_left else chars['h']
            line += chars['h'] * (rect.width - 2)
            line += chars['tr'] if border.show_right else chars['h']
            renderer.buffer.append(renderer.style_text(line, style))
        
        # Side borders
        for i in range(1, rect.height - 1):
            if border.show_left:
                renderer.move_cursor(rect.x, rect.y + i)
                renderer.buffer.append(renderer.style_text(chars['v'], style))
            if border.show_right:
                renderer.move_cursor(rect.x + rect.width - 1, rect.y + i)
                renderer.buffer.append(renderer.style_text(chars['v'], style))
        
        # Bottom border
        if border.show_bottom:
            renderer.move_cursor(rect.x, rect.y + rect.height - 1)
            line = chars['bl'] if border.show_left else chars['h']
            line += chars['h'] * (rect.width - 2)
            line += chars['br'] if border.show_right else chars['h']
            renderer.buffer.append(renderer.style_text(line, style))
    
    def render_shadow(self, renderer, rect):
        """Render shadow effect."""
        if not self.widget_style.shadow.enabled:
            return
        
        from ..core.renderer import Style
        
        shadow = self.widget_style.shadow
        style = Style(fg=shadow.color)
        
        # Right shadow
        for i in range(shadow.offset_y, rect.height):
            renderer.move_cursor(rect.x + rect.width, rect.y + i)
            renderer.buffer.append(renderer.style_text(shadow.char * shadow.offset_x, style))
        
        # Bottom shadow
        renderer.move_cursor(rect.x + shadow.offset_x, rect.y + rect.height)
        renderer.buffer.append(renderer.style_text(shadow.char * rect.width, style))

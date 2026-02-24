"""Theme system for styling widgets."""
from dataclasses import dataclass
from typing import Dict
from .renderer import Style


@dataclass
class ColorScheme:
    """Color scheme for theme."""
    primary: str = 'bright_cyan'
    secondary: str = 'bright_blue'
    success: str = 'bright_green'
    warning: str = 'bright_yellow'
    error: str = 'bright_red'
    info: str = 'bright_blue'
    text: str = 'white'
    text_dim: str = 'bright_black'
    background: str = 'black'
    border: str = 'bright_blue'
    focus: str = 'bright_cyan'
    selection: str = 'bright_white'


class Theme:
    """Theme configuration for widgets."""
    
    def __init__(self, name: str = "default", colors: ColorScheme = None):
        self.name = name
        self.colors = colors or ColorScheme()
        self._styles_cache = {}
    
    def get_style(self, style_name: str, **overrides) -> Style:
        """Get style by name with optional overrides."""
        cache_key = (style_name, tuple(sorted(overrides.items())))
        
        if cache_key in self._styles_cache:
            return self._styles_cache[cache_key]
        
        style = self._create_style(style_name)
        
        # Apply overrides
        for key, value in overrides.items():
            setattr(style, key, value)
        
        self._styles_cache[cache_key] = style
        return style
    
    def _create_style(self, style_name: str) -> Style:
        """Create style based on name."""
        styles = {
            # Text styles
            'text': Style(fg=self.colors.text),
            'text_dim': Style(fg=self.colors.text_dim),
            'text_bold': Style(fg=self.colors.text, bold=True),
            'text_primary': Style(fg=self.colors.primary, bold=True),
            
            # Interactive elements
            'button': Style(fg='white', bg=self.colors.primary, bold=True),
            'button_focused': Style(fg='black', bg=self.colors.focus, bold=True),
            'button_pressed': Style(fg='white', bg=self.colors.secondary, bold=True),
            
            # Selection
            'selected': Style(fg='black', bg=self.colors.selection, bold=True),
            'focused': Style(fg=self.colors.focus, bold=True),
            'normal': Style(fg=self.colors.text),
            
            # Status
            'success': Style(fg=self.colors.success, bold=True),
            'warning': Style(fg=self.colors.warning, bold=True),
            'error': Style(fg=self.colors.error, bold=True),
            'info': Style(fg=self.colors.info, bold=True),
            
            # UI elements
            'border': Style(fg=self.colors.border),
            'title': Style(fg=self.colors.primary, bold=True),
            'label': Style(fg=self.colors.text),
            'placeholder': Style(fg=self.colors.text_dim),
            
            # Progress
            'progress_bar': Style(fg='black', bg=self.colors.success, bold=True),
            'progress_empty': Style(fg=self.colors.text_dim),
            'spinner': Style(fg=self.colors.primary, bold=True),
            
            # Input
            'input': Style(fg=self.colors.text),
            'input_cursor': Style(fg='black', bg='white'),
            'checkbox': Style(fg=self.colors.primary, bold=True),
            'radio': Style(fg=self.colors.primary, bold=True),
            
            # Table
            'table_header': Style(fg='black', bg=self.colors.primary, bold=True),
            'table_row': Style(fg=self.colors.text),
            'table_selected': Style(fg='black', bg=self.colors.selection, bold=True),
        }
        
        return styles.get(style_name, Style(fg=self.colors.text))


# Predefined themes
class Themes:
    """Collection of predefined themes."""
    
    @staticmethod
    def default() -> Theme:
        """Default cyan theme."""
        return Theme("default", ColorScheme())
    
    @staticmethod
    def dark() -> Theme:
        """Dark theme with muted colors."""
        return Theme("dark", ColorScheme(
            primary='cyan',
            secondary='blue',
            success='green',
            warning='yellow',
            error='red',
            info='blue',
            text='white',
            text_dim='bright_black',
            border='bright_black',
            focus='cyan',
            selection='white'
        ))
    
    @staticmethod
    def light() -> Theme:
        """Light theme (for light terminals)."""
        return Theme("light", ColorScheme(
            primary='blue',
            secondary='cyan',
            success='green',
            warning='yellow',
            error='red',
            info='blue',
            text='black',
            text_dim='bright_black',
            border='black',
            focus='blue',
            selection='black'
        ))
    
    @staticmethod
    def purple() -> Theme:
        """Purple/magenta theme."""
        return Theme("purple", ColorScheme(
            primary='bright_magenta',
            secondary='magenta',
            success='bright_green',
            warning='bright_yellow',
            error='bright_red',
            info='bright_cyan',
            text='white',
            text_dim='bright_black',
            border='magenta',
            focus='bright_magenta',
            selection='bright_white'
        ))
    
    @staticmethod
    def matrix() -> Theme:
        """Matrix green theme."""
        return Theme("matrix", ColorScheme(
            primary='bright_green',
            secondary='green',
            success='bright_green',
            warning='bright_yellow',
            error='bright_red',
            info='bright_cyan',
            text='green',
            text_dim='bright_black',
            border='green',
            focus='bright_green',
            selection='bright_white'
        ))
    
    @staticmethod
    def ocean() -> Theme:
        """Ocean blue theme."""
        return Theme("ocean", ColorScheme(
            primary='bright_blue',
            secondary='cyan',
            success='bright_green',
            warning='bright_yellow',
            error='bright_red',
            info='bright_cyan',
            text='bright_cyan',
            text_dim='blue',
            border='blue',
            focus='bright_cyan',
            selection='bright_white'
        ))
    
    @staticmethod
    def fire() -> Theme:
        """Fire red/orange theme."""
        return Theme("fire", ColorScheme(
            primary='bright_red',
            secondary='red',
            success='bright_green',
            warning='bright_yellow',
            error='bright_red',
            info='bright_cyan',
            text='bright_yellow',
            text_dim='red',
            border='red',
            focus='bright_yellow',
            selection='bright_white'
        ))


# Global theme instance
_current_theme = Themes.default()


def get_theme() -> Theme:
    """Get current global theme."""
    return _current_theme


def set_theme(theme: Theme):
    """Set global theme."""
    global _current_theme
    _current_theme = theme


def apply_theme_to_widget(widget, theme: Theme = None):
    """Apply theme styles to widget."""
    if theme is None:
        theme = get_theme()
    
    # Apply theme based on widget type
    widget_type = type(widget).__name__
    
    if widget_type == 'Menu':
        widget.style_normal = theme.get_style('normal')
        widget.style_selected = theme.get_style('selected')
        widget.style_title = theme.get_style('title')
        widget.style_border = theme.get_style('border')
        widget.style_key = theme.get_style('focused')
    
    elif widget_type == 'ProgressBar':
        widget.style_bar = theme.get_style('progress_bar')
        widget.style_empty = theme.get_style('progress_empty')
        widget.style_text = theme.get_style('text_bold')
    
    elif widget_type == 'Spinner':
        widget.style_spinner = theme.get_style('spinner')
        widget.style_text = theme.get_style('text')
    
    elif widget_type == 'StatusIndicator':
        # Status indicators use their own colors
        pass
    
    elif widget_type == 'Checkbox':
        widget.style_box = theme.get_style('checkbox')
        widget.style_label = theme.get_style('label')
        widget.style_selected = theme.get_style('focused')
    
    elif widget_type == 'RadioGroup':
        widget.style_radio = theme.get_style('radio')
        widget.style_label = theme.get_style('label')
        widget.style_selected = theme.get_style('focused')
    
    elif widget_type == 'Button':
        widget.style_normal = theme.get_style('button')
        widget.style_focused = theme.get_style('button_focused')
        widget.style_pressed = theme.get_style('button_pressed')
    
    elif widget_type == 'TextInput':
        widget.style_label = theme.get_style('text_bold')
        widget.style_input = theme.get_style('input')
        widget.style_placeholder = theme.get_style('placeholder')
        widget.style_cursor = theme.get_style('input_cursor')
    
    elif widget_type == 'Table':
        widget.style_header = theme.get_style('table_header')
        widget.style_row = theme.get_style('table_row')
        widget.style_selected = theme.get_style('table_selected')
        widget.style_border = theme.get_style('border')

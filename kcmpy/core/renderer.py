"""Core rendering engine for CUI framework."""
import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Style:
    """Style configuration for text rendering."""
    fg: str = None
    bg: str = None
    bold: bool = False
    italic: bool = False
    underline: bool = False


class Renderer:
    """ANSI-based terminal renderer with modern features."""
    
    COLORS = {
        'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
        'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37,
        'bright_black': 90, 'bright_red': 91, 'bright_green': 92,
        'bright_yellow': 93, 'bright_blue': 94, 'bright_magenta': 95,
        'bright_cyan': 96, 'bright_white': 97
    }
    
    def __init__(self):
        self.buffer: List[str] = []
        self.width, self.height = self.get_terminal_size()
        self.start_line = 0
        self.frame_buffer = {}  # {(x, y): text} for double buffering
    
    def get_terminal_size(self) -> Tuple[int, int]:
        """Get current terminal dimensions."""
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return 80, 24
    
    def style_text(self, text: str, style: Style) -> str:
        """Apply ANSI styling to text."""
        codes = []
        
        if style.bold:
            codes.append('1')
        if style.italic:
            codes.append('3')
        if style.underline:
            codes.append('4')
        if style.fg and style.fg in self.COLORS:
            codes.append(str(self.COLORS[style.fg]))
        if style.bg and style.bg in self.COLORS:
            codes.append(str(self.COLORS[style.bg] + 10))
        
        if codes:
            return f"\033[{';'.join(codes)}m{text}\033[0m"
        return text
    
    def move_cursor(self, x: int, y: int):
        """Move cursor to position."""
        self.buffer.append(f'\033[{y};{x}H')
    
    def hide_cursor(self):
        """Hide terminal cursor."""
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
    
    def show_cursor(self):
        """Show terminal cursor."""
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
    
    def save_cursor(self):
        """Save current cursor position."""
        sys.stdout.write('\033[s')
        sys.stdout.flush()
    
    def restore_cursor(self):
        """Restore saved cursor position."""
        sys.stdout.write('\033[u')
        sys.stdout.flush()
    
    def render(self):
        """Flush buffer to screen."""
        output = ''.join(self.buffer)
        sys.stdout.write(output)
        sys.stdout.flush()
        self.buffer.clear()

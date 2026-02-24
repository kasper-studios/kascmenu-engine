"""Progress bars and loading indicators."""
from ..core.component import Component, Rect
from ..core.renderer import Style
import platform
import time


class ProgressBar(Component):
    """Animated progress bar with percentage."""
    
    def __init__(self, rect: Rect, value: float = 0.0, label: str = ""):
        super().__init__(rect)
        self.value = max(0.0, min(1.0, value))  # 0.0 to 1.0
        self.label = label
        self.style_bar = Style(fg='black', bg='bright_green', bold=True)
        self.style_empty = Style(fg='bright_black')
        self.style_text = Style(fg='white', bold=True)
        self.is_windows = platform.system() == 'Windows'
        self.show_percentage = True
        self.animated = False
        self.animation_offset = 0
    
    def set_value(self, value: float):
        """Set progress value (0.0 to 1.0)."""
        self.value = max(0.0, min(1.0, value))
    
    def update(self, delta_time: float):
        """Update animation."""
        if self.animated:
            self.animation_offset = (self.animation_offset + delta_time * 2) % 1.0
        super().update(delta_time)
    
    def render(self, renderer):
        """Render progress bar."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        # Label
        if self.label:
            renderer.move_cursor(self.rect.x, y)
            renderer.buffer.append(renderer.style_text(self.label, self.style_text))
            y += 1
        
        # Progress bar
        renderer.move_cursor(self.rect.x, y)
        
        bar_width = self.rect.width - 8 if self.show_percentage else self.rect.width
        filled = int(bar_width * self.value)
        empty = bar_width - filled
        
        # Bar characters
        if self.is_windows:
            fill_char = '#'
            empty_char = '-'
        else:
            fill_char = '█'
            empty_char = '░'
        
        # Build bar
        bar = '['
        bar += renderer.style_text(fill_char * filled, self.style_bar)
        bar += renderer.style_text(empty_char * empty, self.style_empty)
        bar += ']'
        
        renderer.buffer.append(bar)
        
        # Percentage
        if self.show_percentage:
            percentage = f" {int(self.value * 100):3d}%"
            renderer.buffer.append(renderer.style_text(percentage, self.style_text))


class Spinner(Component):
    """Animated loading spinner."""
    
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'box': ['◰', '◳', '◲', '◱'],
        'dots_simple': ['.  ', '.. ', '...', ' ..', '  .', '   '],
        'ascii': ['|', '/', '-', '\\'],
    }
    
    def __init__(self, rect: Rect, label: str = "Loading", style: str = 'dots'):
        super().__init__(rect)
        self.label = label
        self.style_spinner = Style(fg='bright_cyan', bold=True)
        self.style_text = Style(fg='white')
        self.is_windows = platform.system() == 'Windows'
        
        # Use ASCII spinner on Windows
        if self.is_windows and style not in ['ascii', 'line', 'dots_simple']:
            style = 'ascii'
        
        self.frames = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self.frame_index = 0
        self.last_update = time.time()
        self.frame_delay = 0.1  # seconds
    
    def update(self, delta_time: float):
        """Update spinner animation."""
        current_time = time.time()
        if current_time - self.last_update >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update = current_time
        super().update(delta_time)
    
    def render(self, renderer):
        """Render spinner."""
        if not self.visible:
            return
        
        renderer.move_cursor(self.rect.x, self.rect.y)
        
        frame = self.frames[self.frame_index]
        spinner_text = renderer.style_text(frame, self.style_spinner)
        label_text = renderer.style_text(f" {self.label}", self.style_text)
        
        renderer.buffer.append(spinner_text + label_text)


class MultiProgressBar(Component):
    """Multiple progress bars with labels."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        self.bars = []  # List of (label, value) tuples
        self.style_label = Style(fg='bright_white')
        self.style_bar = Style(fg='black', bg='bright_green', bold=True)
        self.style_empty = Style(fg='bright_black')
        self.is_windows = platform.system() == 'Windows'
    
    def add_bar(self, label: str, value: float = 0.0):
        """Add a progress bar."""
        self.bars.append([label, max(0.0, min(1.0, value))])
    
    def set_bar(self, index: int, value: float):
        """Update bar value."""
        if 0 <= index < len(self.bars):
            self.bars[index][1] = max(0.0, min(1.0, value))
    
    def set_bar_by_label(self, label: str, value: float):
        """Update bar by label."""
        for bar in self.bars:
            if bar[0] == label:
                bar[1] = max(0.0, min(1.0, value))
                break
    
    def render(self, renderer):
        """Render all progress bars."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        for label, value in self.bars[:self.rect.height]:
            renderer.move_cursor(self.rect.x, y)
            
            # Label (fixed width)
            label_width = 15
            label_text = label[:label_width].ljust(label_width)
            renderer.buffer.append(renderer.style_text(label_text, self.style_label))
            renderer.buffer.append(' ')
            
            # Progress bar
            bar_width = self.rect.width - label_width - 8
            filled = int(bar_width * value)
            empty = bar_width - filled
            
            if self.is_windows:
                fill_char = '#'
                empty_char = '-'
            else:
                fill_char = '█'
                empty_char = '░'
            
            bar = '['
            bar += renderer.style_text(fill_char * filled, self.style_bar)
            bar += renderer.style_text(empty_char * empty, self.style_empty)
            bar += f'] {int(value * 100):3d}%'
            
            renderer.buffer.append(bar)
            y += 1


class StatusIndicator(Component):
    """Status indicator with icon and message."""
    
    STATUS_ICONS = {
        'success': ('✓', 'bright_green'),
        'error': ('✗', 'bright_red'),
        'warning': ('⚠', 'bright_yellow'),
        'info': ('ℹ', 'bright_blue'),
        'loading': ('⟳', 'bright_cyan'),
    }
    
    STATUS_ICONS_ASCII = {
        'success': ('[OK]', 'bright_green'),
        'error': ('[X]', 'bright_red'),
        'warning': ('[!]', 'bright_yellow'),
        'info': ('[i]', 'bright_blue'),
        'loading': ('[~]', 'bright_cyan'),
    }
    
    def __init__(self, rect: Rect, status: str = 'info', message: str = ""):
        super().__init__(rect)
        self.status = status
        self.message = message
        self.is_windows = platform.system() == 'Windows'
    
    def set_status(self, status: str, message: str = None):
        """Update status."""
        self.status = status
        if message is not None:
            self.message = message
    
    def render(self, renderer):
        """Render status indicator."""
        if not self.visible:
            return
        
        renderer.move_cursor(self.rect.x, self.rect.y)
        
        icons = self.STATUS_ICONS_ASCII if self.is_windows else self.STATUS_ICONS
        icon, color = icons.get(self.status, icons['info'])
        
        icon_style = Style(fg=color, bold=True)
        icon_text = renderer.style_text(icon, icon_style)
        
        message_style = Style(fg='white')
        message_text = renderer.style_text(f" {self.message}", message_style)
        
        # Pad with spaces to clear old content
        full_text = icon + " " + self.message
        padded = full_text.ljust(self.rect.width)
        
        renderer.buffer.append(renderer.style_text(icon, icon_style) + 
                             renderer.style_text(f" {self.message}".ljust(self.rect.width - len(icon)), message_style))

"""Interactive menu widgets."""
from ..core.component import Component, Rect
from ..core.renderer import Style
from ..events.event_system import Event, EventType
from typing import List, Callable, Optional
import platform


class MenuItem:
    """Single menu item."""
    
    def __init__(self, label: str, callback: Optional[Callable] = None, key: str = None):
        self.label = label
        self.callback = callback
        self.key = key  # Keyboard shortcut


class Menu(Component):
    """Interactive menu with keyboard navigation."""
    
    def __init__(self, rect: Rect, title: str = "", items: List[MenuItem] = None):
        super().__init__(rect)
        self.title = title
        self.items = items or []
        self.selected_index = 0
        self.style_normal = Style(fg='white')
        self.style_selected = Style(fg='black', bg='bright_cyan', bold=True)
        self.style_title = Style(fg='bright_yellow', bold=True)
        self.style_border = Style(fg='bright_blue')
        self.style_key = Style(fg='bright_green')
        
        # Use ASCII for Windows
        self.is_windows = platform.system() == 'Windows'
    
    def add_item(self, item: MenuItem):
        """Add menu item."""
        self.items.append(item)
    
    def handle_event(self, event: Event) -> bool:
        """Handle keyboard events."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        # Arrow navigation
        if key == '\x1b[A':  # Up arrow
            self.selected_index = (self.selected_index - 1) % len(self.items)
            return True
        elif key == '\x1b[B':  # Down arrow
            self.selected_index = (self.selected_index + 1) % len(self.items)
            return True
        elif key == '\r' or key == '\n':  # Enter
            if self.items[self.selected_index].callback:
                self.items[self.selected_index].callback()
            return True
        else:
            # Check for keyboard shortcuts
            for i, item in enumerate(self.items):
                if item.key and key == item.key:
                    self.selected_index = i
                    if item.callback:
                        item.callback()
                    return True
        
        return False
    
    def render(self, renderer):
        """Render menu."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        # Title with border
        if self.title:
            renderer.move_cursor(self.rect.x, y)
            
            if self.is_windows:
                # ASCII border for Windows
                title_line = f"+== {self.title} ==+"
            else:
                # Unicode border
                title_line = f"╔══ {self.title} ══╗"
            
            # Center and pad
            padding = (self.rect.width - len(title_line)) // 2
            line = ' ' * padding + title_line
            renderer.buffer.append(renderer.style_text(line, self.style_title))
            y += 1
        
        # Menu items
        for i, item in enumerate(self.items):
            renderer.move_cursor(self.rect.x, y)
            
            # Selection indicator
            if self.is_windows:
                indicator = "> " if i == self.selected_index else "  "
            else:
                indicator = "▶ " if i == self.selected_index else "  "
            
            # Keyboard shortcut
            key_hint = f"[{item.key}] " if item.key else ""
            
            # Full line
            line = f"{indicator}{key_hint}{item.label}"
            
            # Pad to width
            line = line.ljust(self.rect.width)
            
            # Apply style
            style = self.style_selected if i == self.selected_index else self.style_normal
            
            if item.key and i != self.selected_index:
                # Highlight key separately
                key_styled = renderer.style_text(f"[{item.key}]", self.style_key)
                line_text = f"{indicator}{key_styled} {item.label}"
                padding_needed = self.rect.width - len(f"{indicator}[{item.key}] {item.label}")
                line_text += ' ' * padding_needed
                renderer.buffer.append(line_text)
            else:
                renderer.buffer.append(renderer.style_text(line, style))
            
            y += 1
        
        # Bottom border
        if self.title:
            renderer.move_cursor(self.rect.x, y)
            
            if self.is_windows:
                bottom = "+" + "=" * (self.rect.width - 2) + "+"
            else:
                bottom = "╚" + "═" * (self.rect.width - 2) + "╝"
            
            padding = (self.rect.width - len(bottom)) // 2
            line = ' ' * padding + bottom
            renderer.buffer.append(renderer.style_text(line, self.style_border))


class SelectList(Component):
    """Simple selection list without borders."""
    
    def __init__(self, rect: Rect, items: List[str] = None):
        super().__init__(rect)
        self.items = items or []
        self.selected_index = 0
        self.style_normal = Style(fg='white')
        self.style_selected = Style(fg='black', bg='bright_white', bold=True)
        self.is_windows = platform.system() == 'Windows'
    
    def handle_event(self, event: Event) -> bool:
        """Handle keyboard events."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        if key == '\x1b[A':  # Up
            self.selected_index = (self.selected_index - 1) % len(self.items)
            return True
        elif key == '\x1b[B':  # Down
            self.selected_index = (self.selected_index + 1) % len(self.items)
            return True
        
        return False
    
    def render(self, renderer):
        """Render selection list."""
        if not self.visible:
            return
        
        for i, item in enumerate(self.items[:self.rect.height]):
            renderer.move_cursor(self.rect.x, self.rect.y + i)
            
            if self.is_windows:
                prefix = "> " if i == self.selected_index else "  "
            else:
                prefix = "▶ " if i == self.selected_index else "  "
            
            line = f"{prefix}{item}".ljust(self.rect.width)
            
            style = self.style_selected if i == self.selected_index else self.style_normal
            renderer.buffer.append(renderer.style_text(line, style))

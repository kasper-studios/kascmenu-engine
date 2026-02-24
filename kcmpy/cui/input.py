"""Input widgets for user interaction."""
from ..core.component import Component, Rect
from ..core.renderer import Style
from ..events.event_system import Event, EventType
from typing import List, Callable, Optional
import platform


class TextInput(Component):
    """Single-line text input field."""
    
    def __init__(self, rect: Rect, label: str = "", placeholder: str = ""):
        super().__init__(rect)
        self.label = label
        self.placeholder = placeholder
        self.value = ""
        self.cursor_pos = 0
        self.style_label = Style(fg='bright_white', bold=True)
        self.style_input = Style(fg='white')
        self.style_placeholder = Style(fg='bright_black')
        self.style_cursor = Style(fg='black', bg='white')
        self.max_length = 100
    
    def handle_event(self, event: Event) -> bool:
        """Handle keyboard input."""
        if not self.focused or event.type != EventType.KEY_PRESS:
            return False

        key = event.data.get('key', '')

        # Backspace
        if key == '\x7f' or key == '\x08':
            if self.cursor_pos > 0:
                self.value = self.value[:self.cursor_pos-1] + self.value[self.cursor_pos:]
                self.cursor_pos -= 1
            return True

        # Delete
        elif key == '\x1b[3~':
            if self.cursor_pos < len(self.value):
                self.value = self.value[:self.cursor_pos] + self.value[self.cursor_pos+1:]
            return True

        # Left arrow
        elif key == '\x1b[D':
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
            return True

        # Right arrow
        elif key == '\x1b[C':
            if self.cursor_pos < len(self.value):
                self.cursor_pos += 1
            return True

        # Home
        elif key == '\x1b[H':
            self.cursor_pos = 0
            return True

        # End
        elif key == '\x1b[F':
            self.cursor_pos = len(self.value)
            return True

        # Regular character (including Unicode/Cyrillic)
        elif len(self.value) < self.max_length:
            # Check if it's a printable character (not control character)
            # Allow all Unicode characters except control characters
            if key and not key.startswith('\x1b') and key not in ('\r', '\n', '\t'):
                # Additional check: skip non-printable ASCII control chars
                if len(key) == 1 and ord(key) < 32:
                    return False
                
                self.value = self.value[:self.cursor_pos] + key + self.value[self.cursor_pos:]
                self.cursor_pos += 1
                return True

        return False
    
    def render(self, renderer):
        """Render text input."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        # Label
        if self.label:
            renderer.move_cursor(self.rect.x, y)
            renderer.buffer.append(renderer.style_text(self.label, self.style_label))
            y += 1
        
        # Input field
        renderer.move_cursor(self.rect.x, y)
        
        display_text = self.value if self.value else self.placeholder
        style = self.style_input if self.value else self.style_placeholder
        
        # Show cursor if focused
        if self.focused and self.value:
            before = self.value[:self.cursor_pos]
            cursor = self.value[self.cursor_pos] if self.cursor_pos < len(self.value) else ' '
            after = self.value[self.cursor_pos+1:]
            
            renderer.buffer.append(renderer.style_text(before, style))
            renderer.buffer.append(renderer.style_text(cursor, self.style_cursor))
            renderer.buffer.append(renderer.style_text(after, style))
        else:
            renderer.buffer.append(renderer.style_text(display_text[:self.rect.width], style))


class Checkbox(Component):
    """Checkbox with label."""
    
    def __init__(self, rect: Rect, label: str = "", checked: bool = False):
        super().__init__(rect)
        self.label = label
        self.checked = checked
        self.style_box = Style(fg='bright_cyan', bold=True)
        self.style_label = Style(fg='white')
        self.style_selected = Style(fg='bright_white', bold=True)
        self.is_windows = platform.system() == 'Windows'
        self.on_change: Optional[Callable] = None
    
    def handle_event(self, event: Event) -> bool:
        """Handle space/enter to toggle."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        if key == ' ' or key == '\r' or key == '\n':
            self.checked = not self.checked
            if self.on_change:
                self.on_change(self.checked)
            return True
        
        return False
    
    def render(self, renderer):
        """Render checkbox."""
        if not self.visible:
            return
        
        renderer.move_cursor(self.rect.x, self.rect.y)
        
        # Checkbox
        if self.is_windows:
            box = '[X]' if self.checked else '[ ]'
        else:
            box = '[✓]' if self.checked else '[ ]'
        
        style = self.style_selected if self.focused else self.style_box
        renderer.buffer.append(renderer.style_text(box, style))
        
        # Label
        label_style = self.style_selected if self.focused else self.style_label
        renderer.buffer.append(renderer.style_text(f" {self.label}", label_style))


class RadioGroup(Component):
    """Radio button group."""
    
    def __init__(self, rect: Rect, options: List[str] = None):
        super().__init__(rect)
        self.options = options or []
        self.selected_index = 0
        self.style_radio = Style(fg='bright_cyan', bold=True)
        self.style_label = Style(fg='white')
        self.style_selected = Style(fg='bright_white', bold=True)
        self.is_windows = platform.system() == 'Windows'
        self.on_change: Optional[Callable] = None
    
    def handle_event(self, event: Event) -> bool:
        """Handle arrow keys and space/enter."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        if key == '\x1b[A':  # Up
            self.selected_index = (self.selected_index - 1) % len(self.options)
            if self.on_change:
                self.on_change(self.selected_index)
            return True
        elif key == '\x1b[B':  # Down
            self.selected_index = (self.selected_index + 1) % len(self.options)
            if self.on_change:
                self.on_change(self.selected_index)
            return True
        elif key == ' ' or key == '\r' or key == '\n':
            if self.on_change:
                self.on_change(self.selected_index)
            return True
        
        return False
    
    def render(self, renderer):
        """Render radio group."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        for i, option in enumerate(self.options[:self.rect.height]):
            renderer.move_cursor(self.rect.x, y)
            
            # Radio button
            if self.is_windows:
                radio = '(*)' if i == self.selected_index else '( )'
            else:
                radio = '(●)' if i == self.selected_index else '( )'
            
            is_focused = self.focused and i == self.selected_index
            style = self.style_selected if is_focused else self.style_radio
            renderer.buffer.append(renderer.style_text(radio, style))
            
            # Label
            label_style = self.style_selected if is_focused else self.style_label
            renderer.buffer.append(renderer.style_text(f" {option}", label_style))
            y += 1


class Button(Component):
    """Clickable button."""
    
    def __init__(self, rect: Rect, label: str = "", callback: Optional[Callable] = None):
        super().__init__(rect)
        self.label = label
        self.callback = callback
        self.style_normal = Style(fg='white', bg='bright_blue', bold=True)
        self.style_focused = Style(fg='black', bg='bright_cyan', bold=True)
        self.style_pressed = Style(fg='white', bg='blue', bold=True)
        self.pressed = False
    
    def handle_event(self, event: Event) -> bool:
        """Handle enter/space to activate."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        if key == ' ' or key == '\r' or key == '\n':
            self.pressed = True
            if self.callback:
                self.callback()
            return True
        
        return False
    
    def render(self, renderer):
        """Render button."""
        if not self.visible:
            return
        
        renderer.move_cursor(self.rect.x, self.rect.y)
        
        # Choose style
        if self.pressed:
            style = self.style_pressed
            self.pressed = False
        elif self.focused:
            style = self.style_focused
        else:
            style = self.style_normal
        
        # Button text
        button_text = f" {self.label} "
        padding = (self.rect.width - len(button_text)) // 2
        full_text = ' ' * padding + button_text + ' ' * padding
        
        renderer.buffer.append(renderer.style_text(full_text, style))

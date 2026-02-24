"""Screen/Scene management system."""
from typing import Dict, Optional, Callable
from .component import Component


class Screen(Component):
    """Base class for screens/scenes."""
    
    def __init__(self, rect, name: str = ""):
        super().__init__(rect)
        self.name = name
        self.screen_manager = None
    
    def on_enter(self):
        """Called when screen becomes active."""
        pass
    
    def on_exit(self):
        """Called when screen becomes inactive."""
        pass
    
    def on_pause(self):
        """Called when screen is paused (another screen pushed on top)."""
        pass
    
    def on_resume(self):
        """Called when screen is resumed (top screen popped)."""
        pass


class ScreenManager:
    """Manages multiple screens with transitions."""
    
    def __init__(self, app):
        self.app = app
        self.screens: Dict[str, Screen] = {}
        self.screen_stack = []
        self.current_screen: Optional[Screen] = None
        self.transition_callback: Optional[Callable] = None
    
    def add_screen(self, name: str, screen: Screen):
        """Register a screen."""
        screen.name = name
        screen.screen_manager = self
        self.screens[name] = screen
    
    def remove_screen(self, name: str):
        """Remove a screen."""
        if name in self.screens:
            del self.screens[name]
    
    def switch_to(self, name: str, clear_stack: bool = True):
        """Switch to a different screen."""
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not found")
        
        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()
        
        # Clear stack if requested
        if clear_stack:
            self.screen_stack.clear()
        
        # Switch to new screen
        self.current_screen = self.screens[name]
        self.current_screen.on_enter()
        
        # Update app root
        self.app.root = self.current_screen
        
        # Clear screen for clean transition
        self.app._clear_screen()
        
        # Call transition callback
        if self.transition_callback:
            self.transition_callback(name)
    
    def push(self, name: str):
        """Push a new screen on top of current (modal-like)."""
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not found")
        
        # Pause current screen
        if self.current_screen:
            self.current_screen.on_pause()
            self.screen_stack.append(self.current_screen.name)
        
        # Activate new screen
        self.current_screen = self.screens[name]
        self.current_screen.on_enter()
        self.app.root = self.current_screen
        
        # Don't clear screen for modal dialogs (they render over previous)
    
    def pop(self):
        """Pop current screen and return to previous."""
        if not self.screen_stack:
            return False
        
        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()
        
        # Return to previous screen
        previous_name = self.screen_stack.pop()
        self.current_screen = self.screens[previous_name]
        self.current_screen.on_resume()
        self.app.root = self.current_screen
        
        # Clear screen for clean transition
        self.app._clear_screen()
        
        return True
    
    def get_current(self) -> Optional[Screen]:
        """Get current active screen."""
        return self.current_screen
    
    def set_transition_callback(self, callback: Callable):
        """Set callback for screen transitions."""
        self.transition_callback = callback


class Dialog(Screen):
    """Modal dialog screen."""
    
    def __init__(self, rect, title: str = "", message: str = ""):
        super().__init__(rect, f"dialog_{id(self)}")
        self.title = title
        self.message = message
        self.result = None
        self.on_close: Optional[Callable] = None
    
    def close(self, result=None):
        """Close dialog and return result."""
        self.result = result
        if self.on_close:
            self.on_close(result)
        if self.screen_manager:
            self.screen_manager.pop()


class MessageDialog(Dialog):
    """Simple message dialog with OK button."""
    
    def __init__(self, rect, title: str, message: str):
        super().__init__(rect, title, message)
        
        from ..cui.widgets import Box, Text
        from ..cui.input import Button
        from .component import Rect as ComponentRect
        
        # Container
        self.box = Box(
            ComponentRect(
                rect.x + rect.width // 4,
                rect.y + rect.height // 3,
                rect.width // 2,
                10
            ),
            title=title,
            border_style='double'
        )
        self.add_child(self.box)
        
        # Message
        self.text = Text(
            ComponentRect(
                self.box.rect.x + 2,
                self.box.rect.y + 2,
                self.box.rect.width - 4,
                5
            ),
            message
        )
        self.box.add_child(self.text)
        
        # OK button
        self.ok_button = Button(
            ComponentRect(
                self.box.rect.x + self.box.rect.width // 2 - 5,
                self.box.rect.y + 7,
                10,
                1
            ),
            "OK",
            lambda: self.close(True)
        )
        self.ok_button.focused = True
        self.box.add_child(self.ok_button)
    
    def handle_event(self, event):
        """Handle events."""
        from ..events.event_system import EventType
        
        if event.type == EventType.KEY_PRESS:
            key = event.data.get('key', '')
            if key == '\r' or key == '\n' or key == ' ':
                self.close(True)
                return True
        
        return self.ok_button.handle_event(event)
    
    def render(self, renderer):
        """Render dialog."""
        # Render semi-transparent background
        from ..core.renderer import Style
        bg_style = Style(fg='bright_black')
        
        for y in range(self.rect.y, self.rect.y + self.rect.height):
            renderer.move_cursor(self.rect.x, y)
            renderer.buffer.append(renderer.style_text('░' * self.rect.width, bg_style))
        
        # Render dialog content
        self.box.render(renderer)


class ConfirmDialog(Dialog):
    """Confirmation dialog with Yes/No buttons."""
    
    def __init__(self, rect, title: str, message: str):
        super().__init__(rect, title, message)
        
        from ..cui.widgets import Box, Text
        from ..cui.input import Button
        from .component import Rect as ComponentRect
        
        # Container
        self.box = Box(
            ComponentRect(
                rect.x + rect.width // 4,
                rect.y + rect.height // 3,
                rect.width // 2,
                10
            ),
            title=title,
            border_style='double'
        )
        self.add_child(self.box)
        
        # Message
        self.text = Text(
            ComponentRect(
                self.box.rect.x + 2,
                self.box.rect.y + 2,
                self.box.rect.width - 4,
                5
            ),
            message
        )
        self.box.add_child(self.text)
        
        # Yes button
        self.yes_button = Button(
            ComponentRect(
                self.box.rect.x + self.box.rect.width // 3 - 5,
                self.box.rect.y + 7,
                10,
                1
            ),
            "Да",
            lambda: self.close(True)
        )
        self.yes_button.focused = True
        self.box.add_child(self.yes_button)
        
        # No button
        self.no_button = Button(
            ComponentRect(
                self.box.rect.x + 2 * self.box.rect.width // 3 - 5,
                self.box.rect.y + 7,
                10,
                1
            ),
            "Нет",
            lambda: self.close(False)
        )
        self.box.add_child(self.no_button)
        
        self.focusable = [self.yes_button, self.no_button]
        self.focused_index = 0
    
    def handle_event(self, event):
        """Handle events."""
        from ..events.event_system import EventType
        
        if event.type == EventType.KEY_PRESS:
            key = event.data.get('key', '')
            
            if key == '\t':
                self.focusable[self.focused_index].focused = False
                self.focused_index = (self.focused_index + 1) % len(self.focusable)
                self.focusable[self.focused_index].focused = True
                return True
        
        return self.focusable[self.focused_index].handle_event(event)
    
    def render(self, renderer):
        """Render dialog."""
        # Render semi-transparent background
        from ..core.renderer import Style
        bg_style = Style(fg='bright_black')
        
        for y in range(self.rect.y, self.rect.y + self.rect.height):
            renderer.move_cursor(self.rect.x, y)
            renderer.buffer.append(renderer.style_text('░' * self.rect.width, bg_style))
        
        # Render dialog content
        self.box.render(renderer)

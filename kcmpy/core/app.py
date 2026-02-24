"""Main application class for CUI framework."""
import time
import os
from .renderer import Renderer
from .component import Component
from .input_handler import InputHandler
from ..events.event_system import EventBus, Event, EventType


class App:
    """Main application controller."""

    def __init__(self, root: Component, inline: bool = True, animated: bool = False):
        self.root = root
        self.renderer = Renderer()
        self.event_bus = EventBus()
        self.input_handler = InputHandler()
        self.running = False
        self.inline = inline
        self.animated = animated  # If true, clear screen on each render
        self.render_area_start = 0

    def run(self):
        """Start the application main loop."""
        self.running = True

        if not self.animated:
            if self.inline:
                print()
                self.render_area_start = 1
        else:
            # Switch to alternate screen buffer (like nano/vim)
            print('\x1b[?1049h', end='', flush=True)

        self.renderer.hide_cursor()

        # Initial render
        if self.animated:
            self._clear_screen()
        self.render()

        last_update = time.time()

        try:
            with self.input_handler:
                while self.running:
                    current_time = time.time()
                    delta_time = current_time - last_update

                    # Update animations or check for updates periodically
                    if delta_time >= 0.1:  # 10 FPS for animations/updates
                        needs_render = False
                        if self.animated:
                            self.root.update(delta_time)
                            needs_render = True
                        else:
                            # Check if component needs update (for async updates like WebSocket)
                            result = self.root.update(delta_time)
                            if result:
                                needs_render = True

                        if needs_render:
                            if self.animated:
                                self._clear_screen()
                            self.render()

                        last_update = current_time

                    # Wait for input (non-blocking with short timeout)
                    key = self.input_handler.get_key(0.05)

                    if key:
                        if key == 'q' or key == '\x03':  # q or Ctrl+C
                            self.stop()
                        else:
                            event = Event(EventType.KEY_PRESS, {'key': key})
                            self.event_bus.emit(event)

                            # Re-render on input
                            if self.root.handle_event(event):
                                if self.animated:
                                    self._clear_screen()
                                self.render()

        finally:
            self.renderer.show_cursor()
            if self.animated:
                # Return to normal screen buffer
                print('\x1b[?1049l', end='', flush=True)
            elif self.inline:
                self.renderer.move_cursor(1, self.render_area_start + self.root.rect.height + 1)
                print()
    
    def _clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def clear_screen(self):
        """Public method to clear screen."""
        self._clear_screen()

    def _get_cursor_line(self) -> int:
        """Get current cursor line (approximate)."""
        return 1

    def update(self, delta_time: float):
        """Update application state."""
        self.root.update(delta_time)

    def render(self):
        """Render frame."""
        self.root.render(self.renderer)
        self.renderer.render()

    def stop(self):
        """Stop the application."""
        self.running = False

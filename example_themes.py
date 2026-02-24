"""Demo of different themes."""
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem
from kcmpy.cui.progress import ProgressBar, StatusIndicator
from kcmpy.cui.input import Button
from kcmpy.core.component import Component
from kcmpy.core.theme import Themes, set_theme, apply_theme_to_widget


class ThemedDemo(Component):
    """Demo with theme switching."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        
        self.app = None  # Will be set later
        self.current_theme_index = 0
        self.themes = [
            ("Default (Cyan)", Themes.default()),
            ("Dark", Themes.dark()),
            ("Light", Themes.light()),
            ("Purple", Themes.purple()),
            ("Matrix", Themes.matrix()),
            ("Ocean", Themes.ocean()),
            ("Fire", Themes.fire()),
        ]
        
        # Title
        self.title = StatusIndicator(
            Rect(2, 2, 60, 1),
            'info',
            f'Current theme: {self.themes[0][0]}'
        )
        self.add_child(self.title)
        
        # Progress bar
        self.progress = ProgressBar(Rect(2, 4, 50, 2), 0.65, "Loading data")
        self.add_child(self.progress)
        
        # Status indicators
        self.status_success = StatusIndicator(Rect(2, 7, 50, 1), 'success', 'Operation successful')
        self.add_child(self.status_success)
        
        self.status_warning = StatusIndicator(Rect(2, 8, 50, 1), 'warning', 'Warning')
        self.add_child(self.status_warning)
        
        self.status_error = StatusIndicator(Rect(2, 9, 50, 1), 'error', 'Error')
        self.add_child(self.status_error)
        
        # Menu
        self.menu = Menu(
            Rect(2, 11, 40, 6),
            title="Menu",
            items=[
                MenuItem("Option 1", None, "1"),
                MenuItem("Option 2", None, "2"),
                MenuItem("Option 3", None, "3"),
            ]
        )
        self.add_child(self.menu)
        
        # Buttons
        self.btn_next = Button(Rect(2, 18, 20, 1), "Next theme", self.next_theme)
        self.add_child(self.btn_next)
        
        self.btn_prev = Button(Rect(24, 18, 20, 1), "Previous theme", self.prev_theme)
        self.add_child(self.btn_prev)
        
        # Info
        self.info = StatusIndicator(
            Rect(2, 20, 60, 1),
            'info',
            'Use buttons or arrows ←/→ to change theme, q to exit'
        )
        self.add_child(self.info)
        
        # Apply initial theme
        self.apply_current_theme()
        
        # Focus management
        self.focusable = [self.btn_next, self.btn_prev]
        self.focused_index = 0
        self.focusable[0].focused = True
    
    def next_theme(self):
        """Switch to next theme."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.apply_current_theme()
        if self.app:
            self.app._clear_screen()
    
    def prev_theme(self):
        """Switch to previous theme."""
        self.current_theme_index = (self.current_theme_index - 1) % len(self.themes)
        self.apply_current_theme()
        if self.app:
            self.app._clear_screen()
    
    def apply_current_theme(self):
        """Apply current theme to all widgets."""
        theme_name, theme = self.themes[self.current_theme_index]
        set_theme(theme)
        
        # Update title
        self.title.message = f'Current theme: {theme_name}'
        
        # Apply theme to all widgets
        for child in self.children:
            apply_theme_to_widget(child, theme)
    
    def handle_event(self, event):
        """Handle events."""
        from kcmpy.events.event_system import EventType
        
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        # Arrow keys for theme switching
        if key == '\x1b[C':  # Right arrow
            self.next_theme()
            return True
        elif key == '\x1b[D':  # Left arrow
            self.prev_theme()
            return True
        
        # Tab for focus switching
        elif key == '\t':
            self.focusable[self.focused_index].focused = False
            self.focused_index = (self.focused_index + 1) % len(self.focusable)
            self.focusable[self.focused_index].focused = True
            return True
        
        # Pass to focused widget
        if self.focusable and self.focused_index < len(self.focusable):
            return self.focusable[self.focused_index].handle_event(event)
        
        return False
    
    def render(self, renderer):
        """Render all widgets."""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(renderer)


def main():
    """Run theme demo."""
    print("=" * 70)
    print("  Theme Demo - KCM Framework")
    print("=" * 70)
    print("\nAvailable themes:")
    print("  1. Default (Cyan) - standard cyan theme")
    print("  2. Dark - dark muted theme")
    print("  3. Light - light theme")
    print("  4. Purple - purple theme")
    print("  5. Matrix - green Matrix-style theme")
    print("  6. Ocean - blue ocean theme")
    print("  7. Fire - red-orange fire theme")
    print("\nControls:")
    print("  ←/→       - switch themes")
    print("  Tab       - switch between buttons")
    print("  Space     - press button")
    print("  q         - exit")
    print("\nPress any key to start...")
    input()
    
    # Clear screen before starting
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    demo = ThemedDemo(Rect(1, 1, 70, 25))
    app = App(demo, inline=False, animated=False)
    demo.app = app  # Set app reference for clearing screen
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    
    print("\nThank you for using KCM!")


if __name__ == "__main__":
    main()


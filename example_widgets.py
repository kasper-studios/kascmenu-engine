"""Demo of all available widgets."""
import time
import threading
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem
from kcmpy.cui.progress import ProgressBar, Spinner, MultiProgressBar, StatusIndicator
from kcmpy.cui.input import Checkbox, RadioGroup, Button
from kcmpy.core.component import Component


class WidgetDemo(Component):
    """Container for widget demo."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        
        # Progress bars
        self.progress1 = ProgressBar(Rect(2, 2, 50, 2), 0.0, "Loading files")
        self.progress1.show_percentage = True
        self.add_child(self.progress1)
        
        self.progress2 = ProgressBar(Rect(2, 5, 50, 2), 0.65, "Processing data")
        self.add_child(self.progress2)
        
        # Multi progress
        self.multi_progress = MultiProgressBar(Rect(2, 8, 60, 4))
        self.multi_progress.add_bar("CPU", 0.45)
        self.multi_progress.add_bar("Memory", 0.78)
        self.multi_progress.add_bar("Disk", 0.23)
        self.add_child(self.multi_progress)
        
        # Spinner
        self.spinner = Spinner(Rect(2, 13, 30, 1), "Connecting to server")
        self.add_child(self.spinner)
        
        # Status indicators
        self.status1 = StatusIndicator(Rect(2, 15, 50, 1), 'success', 'Operation completed successfully')
        self.add_child(self.status1)
        
        self.status2 = StatusIndicator(Rect(2, 16, 50, 1), 'warning', 'Warning: low battery')
        self.add_child(self.status2)
        
        self.status3 = StatusIndicator(Rect(2, 17, 50, 1), 'error', 'Error: database connection failed')
        self.add_child(self.status3)
        
        # Interactive widgets
        self.focusable_widgets = []
        
        # Checkbox
        self.checkbox = Checkbox(Rect(2, 19, 40, 1), "I agree with terms", False)
        self.checkbox.on_change = self.on_checkbox_change
        self.add_child(self.checkbox)
        self.focusable_widgets.append(self.checkbox)
        
        # Radio group
        self.radio = RadioGroup(Rect(2, 21, 40, 4), ["Python", "JavaScript", "Rust", "Go"])
        self.radio.on_change = self.on_radio_change
        self.add_child(self.radio)
        self.focusable_widgets.append(self.radio)
        
        # Button
        self.button = Button(Rect(2, 26, 20, 1), "Click me", self.on_button_click)
        self.add_child(self.button)
        self.focusable_widgets.append(self.button)
        
        # Focus management
        self.focused_index = 0
        if self.focusable_widgets:
            self.focusable_widgets[0].focused = True
        
        # Animation thread
        self.animating = True
        self.anim_thread = threading.Thread(target=self.animate, daemon=True)
        self.anim_thread.start()
        
        # Feedback message
        self.feedback = StatusIndicator(Rect(2, 28, 60, 1), 'info', 'Use Tab to navigate, Space to select')
        self.add_child(self.feedback)
    
    def on_checkbox_change(self, checked):
        """Checkbox change handler."""
        status = 'success' if checked else 'info'
        msg = 'Terms accepted!' if checked else 'Terms not accepted'
        self.feedback.set_status(status, msg)
    
    def on_radio_change(self, idx):
        """Radio change handler."""
        self.feedback.set_status('info', f'Selected language: {self.radio.options[idx]}')
    
    def on_button_click(self):
        """Button click handler."""
        self.feedback.set_status('success', 'Button clicked!')
    
    def handle_event(self, event):
        """Handle events with focus management."""
        from kcmpy.events.event_system import EventType
        
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        # Tab - switch focus
        if key == '\t' or key == '\x1b[Z':  # Tab or Shift+Tab
            if self.focusable_widgets:
                self.focusable_widgets[self.focused_index].focused = False
                self.focused_index = (self.focused_index + 1) % len(self.focusable_widgets)
                self.focusable_widgets[self.focused_index].focused = True
            return True
        
        # Pass event to focused widget
        if self.focusable_widgets and self.focused_index < len(self.focusable_widgets):
            focused = self.focusable_widgets[self.focused_index]
            if focused.handle_event(event):
                return True
        
        return super().handle_event(event)
    
    def animate(self):
        """Animate progress bars."""
        progress = 0.0
        while self.animating:
            progress = (progress + 0.01) % 1.0
            self.progress1.set_value(progress)
            
            # Update multi progress
            import random
            self.multi_progress.set_bar(0, random.random())
            self.multi_progress.set_bar(1, random.random())
            self.multi_progress.set_bar(2, random.random())
            
            time.sleep(0.1)
    
    def render(self, renderer):
        """Render all child widgets."""
        if not self.visible:
            return
        
        # Render all children
        for child in self.children:
            child.render(renderer)
    
    def update(self, delta_time: float):
        """Update animations."""
        self.spinner.update(delta_time)
        super().update(delta_time)


def main():
    """Run widget demo."""
    print("=" * 70)
    print("  Widget Demo - CUI Framework")
    print("=" * 70)
    print("\nControls:")
    print("  Tab       - switch between widgets")
    print("  ↑/↓       - navigate in lists")
    print("  Space     - select/activate")
    print("  q         - exit")
    print("\nPress any key to start...")
    input()
    
    # Clear screen before starting
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    demo = WidgetDemo(Rect(1, 1, 80, 30))
    
    app = App(demo, inline=False, animated=True)  # Use animated mode
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        demo.animating = False
        demo.anim_thread.join(timeout=1)
    
    print("\nThank you for using KCM!")


if __name__ == "__main__":
    main()


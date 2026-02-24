"""Demo of screen management and layouts."""
from kcmpy import App, Rect
from kcmpy.core.screen import Screen, ScreenManager, MessageDialog, ConfirmDialog
from kcmpy.cui.layout import VBox, HBox, Grid
from kcmpy.cui.menu import Menu, MenuItem
from kcmpy.cui.input import Button
from kcmpy.cui.progress import StatusIndicator
from kcmpy.cui.widgets import Box, Text
from kcmpy.core.theme import Themes, set_theme, apply_theme_to_widget


class MainMenuScreen(Screen):
    """Main menu screen."""
    
    def __init__(self, rect):
        super().__init__(rect, "main_menu")
        
        # Title
        self.title = StatusIndicator(
            Rect(2, 2, 60, 1),
            'info',
            'Main Menu - Screen and Layout Demo'
        )
        self.add_child(self.title)
        
        # Menu
        self.menu = Menu(
            Rect(20, 5, 40, 10),
            title="Choose action",
            items=[
                MenuItem("Show VBox Layout", self.show_vbox, "1"),
                MenuItem("Show HBox Layout", self.show_hbox, "2"),
                MenuItem("Show Grid Layout", self.show_grid, "3"),
                MenuItem("Show Dialog", self.show_dialog, "4"),
                MenuItem("Exit", self.confirm_exit, "q"),
            ]
        )
        self.add_child(self.menu)
    
    def show_vbox(self):
        """Show VBox layout demo."""
        self.screen_manager.switch_to("vbox_demo")
    
    def show_hbox(self):
        """Show HBox layout demo."""
        self.screen_manager.switch_to("hbox_demo")
    
    def show_grid(self):
        """Show Grid layout demo."""
        self.screen_manager.switch_to("grid_demo")
    
    def show_dialog(self):
        """Show message dialog."""
        dialog = MessageDialog(
            self.rect,
            "Information",
            "This is a modal dialog example!\n\nНажмите OK для закрытия."
        )
        self.screen_manager.app.screens.add_screen(f"dialog_{id(dialog)}", dialog)
        self.screen_manager.push(f"dialog_{id(dialog)}")
    
    def confirm_exit(self):
        """Show confirmation dialog."""
        dialog = ConfirmDialog(
            self.rect,
            "Подтверждение",
            "Вы уверены что хотите выйти?"
        )
        dialog.on_close = lambda result: self.screen_manager.app.stop() if result else None
        self.screen_manager.app.screens.add_screen(f"confirm_{id(dialog)}", dialog)
        self.screen_manager.push(f"confirm_{id(dialog)}")
    
    def render(self, renderer):
        """Render screen."""
        for child in self.children:
            child.render(renderer)


class VBoxDemoScreen(Screen):
    """VBox layout demonstration."""
    
    def __init__(self, rect):
        super().__init__(rect, "vbox_demo")
        
        # Create VBox layout
        self.layout = VBox(Rect(10, 3, 60, 20), spacing=1)
        
        # Add widgets with different heights
        title = StatusIndicator(Rect(0, 0, 60, 1), 'info', 'VBox Layout Demo - виджеты расположены вертикально')
        self.layout.add(title, height=1)
        
        info1 = StatusIndicator(Rect(0, 0, 60, 1), 'success', 'Виджет 1 - фиксированная высота')
        self.layout.add(info1, height=1)
        
        info2 = StatusIndicator(Rect(0, 0, 60, 1), 'warning', 'Виджет 2 - фиксированная высота')
        self.layout.add(info2, height=1)
        
        info3 = StatusIndicator(Rect(0, 0, 60, 1), 'error', 'Виджет 3 - фиксированная высота')
        self.layout.add(info3, height=1)
        
        # Spacer
        from kcmpy.core.component import Component
        spacer = Component(Rect(0, 0, 60, 0))
        self.layout.add(spacer)  # Flexible - takes remaining space
        
        back_btn = Button(Rect(0, 0, 20, 1), "Назад в меню", self.go_back)
        back_btn.focused = True
        self.layout.add(back_btn, height=1)
        
        self.add_child(self.layout)
        self.back_btn = back_btn
    
    def go_back(self):
        """Return to main menu."""
        self.screen_manager.switch_to("main_menu")
    
    def handle_event(self, event):
        """Handle events."""
        return self.back_btn.handle_event(event)
    
    def render(self, renderer):
        """Render screen."""
        self.layout.render(renderer)


class HBoxDemoScreen(Screen):
    """HBox layout demonstration."""
    
    def __init__(self, rect):
        super().__init__(rect, "hbox_demo")
        
        # Title
        self.title = StatusIndicator(Rect(10, 3, 60, 1), 'info', 'HBox Layout Demo - виджеты расположены горизонтально')
        self.add_child(self.title)
        
        # Create HBox layout
        self.layout = HBox(Rect(10, 7, 60, 10), spacing=2)
        
        # Add widgets with different widths
        from kcmpy.cui.progress import ProgressBar
        
        prog1 = ProgressBar(Rect(0, 0, 0, 10), 0.3, "CPU")
        self.layout.add(prog1, width=15)
        
        prog2 = ProgressBar(Rect(0, 0, 0, 10), 0.7, "Memory")
        self.layout.add(prog2)  # Flexible width
        
        prog3 = ProgressBar(Rect(0, 0, 0, 10), 0.5, "Disk")
        self.layout.add(prog3, width=20)
        
        self.add_child(self.layout)
        
        # Back button
        self.back_btn = Button(Rect(30, 18, 20, 1), "Назад в меню", self.go_back)
        self.back_btn.focused = True
        self.add_child(self.back_btn)
    
    def go_back(self):
        """Return to main menu."""
        self.screen_manager.switch_to("main_menu")
    
    def handle_event(self, event):
        """Handle events."""
        return self.back_btn.handle_event(event)
    
    def render(self, renderer):
        """Render screen."""
        for child in self.children:
            child.render(renderer)


class GridDemoScreen(Screen):
    """Grid layout demonstration."""
    
    def __init__(self, rect):
        super().__init__(rect, "grid_demo")
        
        # Title
        self.title = StatusIndicator(Rect(10, 3, 60, 1), 'info', 'Grid Layout Demo - сетка 3x3')
        self.add_child(self.title)
        
        # Create Grid layout
        self.layout = Grid(Rect(10, 7, 60, 12), rows=3, cols=3, spacing=1)
        
        # Add widgets to grid
        statuses = ['success', 'warning', 'error', 'info', 'success', 'warning', 'error', 'info', 'success']
        
        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                status = StatusIndicator(
                    Rect(0, 0, 0, 0),
                    statuses[idx],
                    f"[{row},{col}]"
                )
                self.layout.add(status, row, col)
        
        self.add_child(self.layout)
        
        # Back button
        self.back_btn = Button(Rect(30, 20, 20, 1), "Назад в меню", self.go_back)
        self.back_btn.focused = True
        self.add_child(self.back_btn)
    
    def go_back(self):
        """Return to main menu."""
        self.screen_manager.switch_to("main_menu")
    
    def handle_event(self, event):
        """Handle events."""
        return self.back_btn.handle_event(event)
    
    def render(self, renderer):
        """Render screen."""
        for child in self.children:
            child.render(renderer)


def main():
    """Run screens demo."""
    print("=" * 70)
    print("  Screen and Layout Demo")
    print("=" * 70)
    print("\nFeatures:")
    print("  • Screen system (Screen Manager)")
    print("  • VBox, HBox, Grid layouts")
    print("  • Modal dialogs")
    print("  • Navigation between screens")
    print("\nPress any key to start...")
    input()
    
    # Clear screen before starting
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Create app with empty root (will be replaced by screen manager)
    from kcmpy.core.component import Component
    app = App(Component(Rect(1, 1, 80, 30)), inline=False, animated=False)
    
    # Create screen manager
    screens = ScreenManager(app)
    app.screens = screens
    
    # Create and register screens
    main_screen = MainMenuScreen(Rect(1, 1, 80, 30))
    vbox_screen = VBoxDemoScreen(Rect(1, 1, 80, 30))
    hbox_screen = HBoxDemoScreen(Rect(1, 1, 80, 30))
    grid_screen = GridDemoScreen(Rect(1, 1, 80, 30))
    
    screens.add_screen("main_menu", main_screen)
    screens.add_screen("vbox_demo", vbox_screen)
    screens.add_screen("hbox_demo", hbox_screen)
    screens.add_screen("grid_demo", grid_screen)
    
    # Start with main menu
    screens.switch_to("main_menu")
    
    # Apply theme
    theme = Themes.default()
    set_theme(theme)
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    
    print("\nСпасибо за использование!")


if __name__ == "__main__":
    main()



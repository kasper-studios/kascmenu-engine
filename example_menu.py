"""Example of interactive menu."""
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem

def on_new():
    print("\n✓ New project created")

def on_open():
    print("\n✓ Project opened")

def on_settings():
    print("\n✓ Settings opened")

def on_exit():
    print("\n✓ Exiting program")
    app.stop()

# Create menu (positioned below the text)
menu = Menu(
    Rect(5, 10, 40, 8),
    title="Main Menu",
    items=[
        MenuItem("New Project", on_new, "n"),
        MenuItem("Open Project", on_open, "o"),
        MenuItem("Settings", on_settings, "s"),
        MenuItem("Exit", on_exit, "q"),
    ]
)

print("=" * 50)
print("Interactive Menu - CUI Framework")
print("=" * 50)
print("\nControls:")
print("  ↑/↓  - navigate")
print("  Enter - select")
print("  n/o/s/q - hotkeys")
print()

# Run application
app = App(menu, inline=True)
try:
    app.run()
except KeyboardInterrupt:
    app.stop()

print("\nThank you for using KCM!")


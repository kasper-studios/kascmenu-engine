# KCM - Modern CUI Framework

A powerful modern framework for creating Console User Interfaces (CUI) in Python and JavaScript.

## 📦 Installation

### Python Version
```bash
# From source (development mode)
pip install -e .

# Or with additional dependencies
pip install -e .[all]

# Check installation
kcm doctor
```

### JavaScript Version
```bash
cd kcmjs
npm install
node example.js
```

**Status:** Python version ✅ ready, JavaScript version ✅ ready (basic widgets)

Details: [INSTALL.md](INSTALL.md)

## 🎨 Features

### CLI Toolchain
- **kcm init** - create project from template
- **kcm run** - run application
- **kcm build** - compile to exe/binary via Nuitka
- **kcm doctor** - check environment
- **kcm** (no args) - interactive menu

### Basic Components
- **Box, Text** - containers and text blocks
- **Menu, SelectList** - interactive menus with navigation

### Progress & Indicators
- **ProgressBar** - progress bar with percentage and animation
- **Spinner** - animated loading spinner (10+ styles)
- **MultiProgressBar** - multiple progress bars simultaneously
- **StatusIndicator** - status with icons (success, error, warning, info)

### Input Widgets
- **TextInput** - text field with cursor
- **Checkbox** - checkbox with callback
- **RadioGroup** - radio button group
- **Button** - clickable button

### Data Display
- **Table** - table with scrolling and highlighting
- **Chart** - ASCII charts
- **TreeView** - hierarchical tree

### Screen System & Layouts
- **ScreenManager** - screen management
- **VBox, HBox** - vertical/horizontal layouts
- **Grid** - grid layout
- **Stack** - component stacking

### Themes
- 7 built-in themes (Default, Dark, Light, Purple, Matrix, Ocean, Fire)
- Customizable colors, styles, borders
- Global theme application

### Key Features
- ✅ Event-driven architecture (no render spam)
- ✅ Focus system and Tab navigation
- ✅ Cross-platform (Windows/Unix)
- ✅ Automatic ASCII/Unicode character selection
- ✅ Cyrillic and Unicode input support
- ✅ Animation support
- ✅ Inline and fullscreen modes
- ✅ Styling (colors, bold, italic, underline)
- ✅ JSON config persistence
- ✅ Standalone exe/binary compilation

## 🚀 Quick Start

### Create New Project

```bash
# Interactive mode
kcm

# Or directly
kcm init my_app
cd my_app
python app.py
```

### Simple Menu
```python
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem

menu = Menu(
    Rect(1, 1, 40, 6),
    title="Main Menu",
    items=[
        MenuItem("New Project", lambda: print("Created!"), "n"),
        MenuItem("Exit", lambda: app.stop(), "q"),
    ]
)

app = App(menu, inline=True)
app.run()
```

## 📚 Examples

- `example_menu.py` - interactive menu
- `example_widgets.py` - demo of all widgets with animation
- `example_screens.py` - screen system and layouts (VBox, HBox, Grid)
- `example_themes.py` - theme demonstration
- `chat_client.py` + `chat_server.py` - WebSocket chat with CUI interface

Run: `python example_widgets.py`

## 💬 WebSocket Chat Demo

Real application demo with WebSocket connection:

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start Server
```bash
python chat_server.py
```
Server starts at `http://localhost:5000` with web interface for monitoring.

### Start Client
```bash
python chat_client.py
```
No additional libraries required, notifications shown in console.
### Chat Features:
- Server address and nickname configuration
- Send and receive messages in real-time
- Message history scrolling (↑/↓)
- User connect/disconnect notifications
- Web interface for server monitoring
- Notification type configuration
- Cyrillic support

## 🎮 Controls

- `q` - exit
- `Tab` - switch focus
- `↑/↓` - navigation
- `Space/Enter` - select

## 📝 License

MIT

---

## 📚 Documentation

- **[README.md](README.md)** - this file, project overview
- **[INSTALL.md](INSTALL.md)** - installation guide
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Nuitka compilation guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - architecture, roadmap, lessons learned
- **[CHANGELOG.md](CHANGELOG.md)** - change history

## 🎯 Project Status

**Version:** 0.1.0  
**Status:** Active Development  
**Date:** 2026-02-24

### What Works
✅ Core framework (Component, Renderer, App, Events)  
✅ 20+ widgets (Menu, Input, Progress, Table, etc.)  
✅ Screen Management (routing, lifecycle, dialogs)  
✅ Layout System (VBox, HBox, Grid, Stack, Anchor)  
✅ Styling & Themes (7 ready themes)  
✅ Real-time Chat (WebSocket + Notifications)  
✅ Cross-platform (Windows, Linux, macOS)  
✅ Unicode/Cyrillic support  

### In Development
🚧 Thread-safe event queue  
🚧 Template screens (FormScreen, ListScreen, etc.)  
🚧 Unit tests  
🚧 API documentation  
🚧 Async funcs

### Roadmap
📋 v0.2 - Stabilization  
📋 v0.3 - Template Screens  
📋 v0.4 - Advanced Widgets  
📋 v1.0 - Production Ready  

Details in [ARCHITECTURE.md](ARCHITECTURE.md)

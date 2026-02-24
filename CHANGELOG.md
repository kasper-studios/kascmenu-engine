# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `kcmpy/core/config.py` - JSON settings persistence system
- `build_nuitka.py` - interactive build system with KCM UI! 🎨
- `build.bat` / `build.sh` - quick compilation scripts
- `BUILD_GUIDE.md` - complete Nuitka compilation guide
- **`kcm_cli.py` - CLI tool for project scaffolding!** 🛠️
- **`kcm` / `kcm.bat` - wrapper scripts for convenient launch**
- **Autosave settings** to `~/.kcm/kcm_chat.json`
- **Interactive CLI mode** - KCM UI menu (dogfooding!)
- **Commands**: `init`, `run`, `build`, `doctor`

### Fixed
- Rendering issues in chat (text artifacts and overlapping)
- win10toast error `WNDPROC return value cannot be converted to LRESULT`
- Screen now clears on updates in ChatScreen
- Improved error handling in NotificationManager
- **Long messages now truncated with "..." instead of breaking layout**
- Messages no longer break chat frame

### Changed
- `chat_client.py` - improved error handling
- Message rendering accounts for window width and truncates long lines
- **build_nuitka.py now uses KCM UI** - framework capabilities demonstration!
- **KCM CLI uses KCM for its UI** - ultimate dogfooding! 🎨

### Planned
- Thread-safe event queue
- Template screens (FormScreen, ListScreen, LogScreen)
- Unit tests for core components
- API documentation
- Hot reload for development

## [0.1.0] - 2026-02-24

### Added - Core Framework
- **Component** - base class for all UI elements
- **Renderer** - ANSI rendering with cross-platform support
- **App** - main loop with event-driven architecture
- **InputHandler** - keyboard handling with Unicode/Cyrillic support
- **EventBus** - event system (KEY_PRESS, MOUSE_CLICK, etc.)

### Added - Screen Management
- **Screen** - base class for screens
- **ScreenManager** - routing between screens (switch_to, push, pop)
- **Dialog** - modal windows (MessageDialog, ConfirmDialog)
- Lifecycle hooks: on_enter, on_exit, on_pause, on_resume

### Added - Widgets (20+)
- **Containers**: Box, Text
- **Menus**: Menu, MenuItem, SelectList
- **Progress**: ProgressBar, Spinner (10+ styles), MultiProgressBar, StatusIndicator
- **Input**: TextInput, Checkbox, RadioGroup, Button
- **Data**: Table, Chart, TreeView

### Added - Layout System
- **VBox** - vertical layout with fixed/flexible heights
- **HBox** - horizontal layout with fixed/flexible widths
- **Grid** - grid with rows x cols and spanning
- **Stack** - z-index layers
- **Anchor** - positioning relative to edges

### Added - Styling & Themes
- **Style** - colors, bold, italic, underline
- **Theme** - Theme system with 7 presets (Default, Dark, Light, Purple, Matrix, Ocean, Fire)
- **WidgetStyle** - padding, margin, border (6 styles), shadow
- **StyledWidget** - mixin for applying styles
- Automatic ASCII/Unicode character selection by platform

### Added - Advanced Features
- **needs_render** - dirty flag system for optimization
- **animated mode** - mode for animated widgets
- **focus system** - Tab navigation between elements
- **async updates** - WebSocket and threading support
- **Unicode/Cyrillic** - full Cyrillic support on Windows (cp866) and Linux (UTF-8)

### Added - Examples
- `example_menu.py` - interactive menu with keyboard shortcuts
- `example_widgets.py` - all widgets demo with animation
- `example_screens.py` - multi-screen app with VBox/HBox/Grid
- `example_themes.py` - all themes demonstration
- `chat_client.py` + `chat_server.py` - WebSocket chat with CUI interface

### Added - Real-world Application: WebSocket Chat
- `chat_server.py` - Flask-SocketIO server with web interface
- `chat_client.py` - basic CUI chat client
- **Features**:
  - Server and nickname configuration via UI
  - Real-time messages via WebSocket
  - Message history with scrolling
  - User join/leave notifications
  - Push notifications (Windows Toast, Linux notify-send)
  - Notification type configuration via checkboxes

### Added - Documentation
- `README.md` - project overview
- `INSTALL.md` - installation guide
- `ARCHITECTURE.md` - architecture, roadmap, lessons learned
- `BUILD_GUIDE.md` - Nuitka compilation guide
- `CHANGELOG.md` - change history

### Fixed
- Rendering without spam (event-driven instead of 60 FPS loop)
- Artifacts during screen transitions (added clear_screen)
- Phantom lines from widgets (removed `\n` from render methods)
- Focus issues (added focused/focusable system)
- Auto-update on WebSocket events (needs_render flag)
- Cyrillic input on Windows (cp866 and multi-byte character support)
- Unicode character handling in TextInput

### Changed
- Component.render() from abstract to concrete with default implementation
- App.run() now periodically checks updates even in non-animated mode
- InputHandler reads multi-byte UTF-8 characters on Windows
- TextInput accepts all Unicode characters except control characters

### Technical Details
- **Lines of Code**: ~6000 (Python + examples + docs)
- **Widgets**: 20+
- **Themes**: 7
- **Examples**: 5
- **Documentation**: 5 files

### Performance
- Event-driven rendering saves CPU
- Dirty flags minimize redraws
- Async updates don't block UI
- Render < 16ms for 60 FPS

### Platform Support
- ✅ Windows 10/11 (cmd, PowerShell, Windows Terminal)
- ✅ Linux (bash, zsh, any ANSI terminal)
- ✅ macOS (Terminal.app, iTerm2)

### Dependencies
- Python 3.7+
- flask >= 3.0.0 (for chat_server)
- flask-socketio >= 5.3.0 (for chat_server)
- python-socketio >= 5.11.0 (for chat_client)
- win10toast >= 0.9 (Optional, for notifications on Windows)

## [0.0.1] - 2026-02-23

### Added
- Initial project version
- Basic framework structure
- Simple menu

---

## Change Types

- **Added** - new features
- **Changed** - changes to existing functionality
- **Deprecated** - functionality that will be removed soon
- **Removed** - removed functionality
- **Fixed** - bug fixes
- **Security** - vulnerability fixes

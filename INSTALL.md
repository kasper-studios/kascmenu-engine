# KCM Framework - Installation

## 📦 Installation via pip

### From PyPI (when published)
```bash
# Basic installation
pip install kascmpy

# With chat support
pip install kascmpy[chat]

# With notifications
pip install kascmpy[notifications]

# With Nuitka for building
pip install kascmpy[build]

# All dependencies
pip install kascmpy[all]

# For development
pip install kascmpy[dev]
```

### From source (now)
```bash
# Clone repository
git clone https://github.com/kasper-studios/kascmenu-engine.git
cd kascmenu-engine

# Install in development mode
pip install -e .

# Or with additional dependencies
pip install -e .[all]
```

### From wheel file (locally)
```bash
# Build package
python setup.py sdist bdist_wheel

# Install from wheel
pip install dist/kascmpy-0.1.0-py3-none-any.whl
```

## 🚀 Quick Start

After installation:

```bash
# Check installation
kcm doctor

# Create new project
kcm init my_app

# Go to project
cd my_app

# Run
python app.py

# Or via CLI
kcm run
```

## 🎨 Interactive Mode

Run CLI without arguments for interactive menu:

```bash
kcm
```

Beautiful menu will appear with options:
- Create new project
- Run project
- Build project
- Check environment
- Exit

## 📋 Dependencies

### Basic (always)
- Python >= 3.7
- No external dependencies!

### Optional

#### For chat (`[chat]`)
- flask >= 3.0.0
- flask-socketio >= 5.3.0
- python-socketio >= 5.11.0

#### For notifications (`[notifications]`)
- win10toast >= 0.9 (Windows only)

#### For building (`[build]`)
- nuitka >= 1.0
- cython >= 3.0.0 (Python 3.12+)

#### For development (`[dev]`)
- pytest >= 7.0
- pytest-cov >= 4.0
- black >= 23.0
- flake8 >= 6.0
- mypy >= 1.0

## 🔧 Verify Installation

```bash
# Check version
python -c "import kcmpy; print(kcmpy.__version__)"

# Check CLI
kcm doctor
```

## 🐛 Troubleshooting

### "kcm command not found"

**Cause:** CLI not in PATH

**Solution:**
```bash
# Show where installed
pip show kascmpy

# Or reinstall
pip install --force-reinstall kascmpy
```

### "No module named 'kcmpy'"

**Cause:** Package not installed

**Solution:**
```bash
pip install kascmpy
# or
pip install -e .  # from source
```

### Dependency issues

**Solution:**
```bash
# Reinstall with dependencies
pip install --force-reinstall kascmpy[all]
```

## 📚 Examples

### Basic usage
```python
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem

menu = Menu(
    Rect(1, 1, 40, 6),
    title="Main Menu",
    items=[
        MenuItem("Item 1", lambda: print("1"), "1"),
        MenuItem("Exit", lambda: app.stop(), "q"),
    ]
)

app = App(menu, inline=True)
app.run()
```

### With screens
```python
from kcmpy import App, Rect
from kcmpy.core.screen import Screen, ScreenManager

class MainScreen(Screen):
    def __init__(self, rect):
        super().__init__(rect, "main")
        # Your code

app = App(...)
screens = ScreenManager(app)
screens.add_screen("main", MainScreen(...))
screens.switch_to("main")
app.run()
```

## 🌍 Platforms

### Windows
✅ Full support
- Windows 10/11
- cmd.exe, PowerShell, Windows Terminal

### Linux
✅ Full support
- Ubuntu, Debian, Fedora, Arch
- bash, zsh, fish

### macOS
✅ Full support
- Terminal.app, iTerm2

## 📖 Additional

### Virtual environment (recommended)
```bash
# Create venv
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install KCM
pip install kascmpy
```

### Update
```bash
pip install --upgrade kascmpy
```

### Uninstall
```bash
pip uninstall kascmpy
```

## 🔗 Links

- [PyPI](https://pypi.org/project/kascmpy/) (when published)
- [GitHub](https://github.com/kasper-studios/kascmenu-engine)
- [Documentation](README.md)
- [Build Guide](BUILD_GUIDE.md)
- [Architecture](ARCHITECTURE.md)

---

**Version:** 0.1.0  
**Date:** 2026-02-24

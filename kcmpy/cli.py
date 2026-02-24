#!/usr/bin/env python3
"""KCM CLI - Project scaffolding and build tool using KCM UI itself!"""
import sys
import shutil
from pathlib import Path
import subprocess
import platform

# Check if running in interactive mode
INTERACTIVE = len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['ui', 'menu'])


def show_banner():
    """Show KCM CLI banner."""
    print("=" * 70)


def cmd_init(project_name: str = None, template: str = "basic"):
    """Create new KCM project."""
    if not project_name:
        project_name = input("Project name: ").strip()
        if not project_name:
            print("❌ Project name is required!")
            return False
    
    # Check if directory exists
    project_path = Path(project_name)
    if project_path.exists():
        print(f"❌ Directory '{project_name}' already exists!")
        return False
    
    print(f"\n🚀 Creating project '{project_name}' with template '{template}'...")
    
    # Create project structure
    try:
        project_path.mkdir(parents=True)
        
        # Create subdirectories
        (project_path / "screens").mkdir()
        (project_path / "widgets").mkdir()
        
        # Create app.py
        app_content = f'''"""
{project_name} - KCM Application
"""
from kcmpy import App, Rect
from kcmpy.core.screen import Screen, ScreenManager
from kcmpy.core.theme import Themes, set_theme
from kcmpy.core.config import Config
from screens.main_screen import MainScreen


def main():
    """Run application."""
    print("=" * 70)
    print("  {project_name}")
    print("=" * 70)
    print("\\nPress any key to start...")
    input()
    
    # Create config
    config = Config(app_name="{project_name.lower()}")
    
    # Create app
    from kcmpy.core.component import Component
    app = App(Component(Rect(1, 1, 80, 30)), inline=False, animated=False)
    
    # Create screen manager
    screens = ScreenManager(app)
    app.screens = screens
    
    # Create and register screens
    main_screen = MainScreen(Rect(1, 1, 80, 30), config)
    screens.add_screen("main", main_screen)
    
    # Start with main screen
    screens.switch_to("main")
    
    # Apply theme
    theme = Themes.default()
    set_theme(theme)
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    
    print("\\nThank you for using {project_name}!")


if __name__ == "__main__":
    main()
'''
        (project_path / "app.py").write_text(app_content, encoding='utf-8')
        
        # Create main_screen.py
        screen_content = '''"""Main screen for application."""
from kcmpy import Rect
from kcmpy.core.screen import Screen
from kcmpy.cui.menu import Menu, MenuItem
from kcmpy.cui.progress import StatusIndicator


class MainScreen(Screen):
    """Main application screen."""
    
    def __init__(self, rect, config):
        super().__init__(rect, "main")
        self.config = config
        
        # Title
        self.title = StatusIndicator(
            Rect(2, 2, rect.width - 4, 1),
            'info',
            'Main Menu'
        )
        self.add_child(self.title)
        
        # Menu
        self.menu = Menu(
            Rect(20, 5, 40, 10),
            title="Choose action",
            items=[
                MenuItem("Settings", self.show_settings, "s"),
                MenuItem("About", self.show_about, "a"),
                MenuItem("Exit", self.exit_app, "q"),
            ]
        )
        self.add_child(self.menu)
    
    def show_settings(self):
        """Show settings."""
        # TODO: Implement settings screen
        pass
    
    def show_about(self):
        """Show about."""
        # TODO: Implement about screen
        pass
    
    def exit_app(self):
        """Exit application."""
        if self.screen_manager and self.screen_manager.app:
            self.screen_manager.app.stop()
    
    def render(self, renderer):
        """Render screen."""
        for child in self.children:
            child.render(renderer)
'''
        (project_path / "screens" / "main_screen.py").write_text(screen_content, encoding='utf-8')
        
        # Create __init__.py files
        (project_path / "screens" / "__init__.py").write_text("", encoding='utf-8')
        (project_path / "widgets" / "__init__.py").write_text("", encoding='utf-8')
        
        # Create requirements.txt
        requirements = '''# KCM Framework
# Install from local: pip install -e path/to/kcmpy

# Or if published:
# kascmpy>=0.1.0
'''
        (project_path / "requirements.txt").write_text(requirements, encoding='utf-8')
        
        # Create config.json
        config = '''{
  "app": {
    "name": "''' + project_name + '''",
    "version": "0.1.0"
  },
  "theme": "default"
}
'''
        (project_path / "config.json").write_text(config, encoding='utf-8')
        
        # Create README.md
        readme = f'''# {project_name}

KCM Application

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Structure

```
{project_name}/
├── app.py              # Entry point
├── screens/            # Application screens
│   └── main_screen.py
├── widgets/            # Custom widgets
├── config.json         # Configuration
└── requirements.txt    # Dependencies
```

## Development

Created with [KCM Framework](https://github.com/kasper-studios/kascmenu-engine)
'''
        (project_path / "README.md").write_text(readme, encoding='utf-8')
        
        print(f"✅ Project '{project_name}' created!")
        print("\nStructure:")
        print(f"  {project_name}/")
        print("  ├── app.py")
        print("  ├── screens/")
        print("  │   └── main_screen.py")
        print("  ├── widgets/")
        print("  ├── config.json")
        print("  ├── requirements.txt")
        print("  └── README.md")
        print("\nNext steps:")
        print(f"  cd {project_name}")
        print("  python app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        # Cleanup on error
        if project_path.exists():
            shutil.rmtree(project_path)
        return False


def cmd_run():
    """Run current project."""
    if not Path("app.py").exists():
        print("❌ app.py not found! Are you in project directory?")
        return False
    
    print("🚀 Running application...")
    try:
        subprocess.run([sys.executable, "app.py"], check=False)
        return True
    except KeyboardInterrupt:
        print("\n⏹️  Stopped")
        return True


def cmd_build():
    """Build current project with Nuitka."""
    if not Path("app.py").exists():
        print("❌ app.py not found! Are you in project directory?")
        return False
    
    # Check Nuitka
    try:
        subprocess.run([sys.executable, "-m", "nuitka", "--version"],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Nuitka not installed!")
        print("Install: pip install nuitka")
        return False
    
    print("🔨 Compiling with Nuitka...")
    
    is_windows = platform.system() == 'Windows'
    project_name = Path.cwd().name
    output_name = f"{project_name}.exe" if is_windows else project_name
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=no-qt",
        "--assume-yes-for-downloads",
        f"--output-filename={output_name}",
        "--output-dir=dist",
        "--lto=yes",
        "--python-flag=no_site",
        "--include-package=kcmpy",
        "--nofollow-import-to=tkinter",
        "--nofollow-import-to=matplotlib",
    ]
    
    if is_windows:
        cmd.append("--windows-console-mode=attach")
    
    cmd.append("app.py")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Compiled: dist/{output_name}")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Compilation error")
        return False


def cmd_doctor():
    """Check environment."""
    print("=" * 70)
    print("🔍 Checking environment...\n")
    
    # Python version
    print(f"Python: {sys.version.split()[0]} ✅")
    
    # Nuitka
    try:
        result = subprocess.run([sys.executable, "-m", "nuitka", "--version"],
                              capture_output=True, text=True, check=True)
        version = result.stdout.strip().split('\n')[0]
        print(f"Nuitka: {version} ✅")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Nuitka: not installed ❌")
        print("  Install: pip install nuitka")
    
    # KCM
    try:
        import kcmpy  # noqa: F401
        print("KCM: installed ✅")
    except ImportError:
        print("KCM: not installed ❌")
        print("  Install from repository")
    
    # Current project
    if Path("app.py").exists():
        print(f"\nCurrent project: {Path.cwd().name} ✅")
    else:
        print("\nCurrent project: not found")
    
    print()
    return True


def show_interactive_menu():
    """Show interactive menu using KCM UI."""
    try:
        from kcmpy import App, Rect
        from kcmpy.cui.menu import Menu, MenuItem
        from kcmpy.cui.progress import StatusIndicator
        from kcmpy.core.component import Component
        from kcmpy.core.theme import Themes, set_theme
        
        class CLIScreen(Component):
            """CLI menu screen."""
            
            def __init__(self, rect):
                super().__init__(rect)
                
                # Title
                self.title = StatusIndicator(
                    Rect(2, 2, rect.width - 4, 1),
                    'info',
                    '🛠️  KCM CLI - Toolchain'
                )
                self.add_child(self.title)
                
                # Menu
                self.menu = Menu(
                    Rect(20, 5, 40, 14),
                    title="Choose action",
                    items=[
                        MenuItem("Create new project", self.new_project, "1"),
                        MenuItem("Run project", self.run_project, "2"),
                        MenuItem("Build project", self.build_project, "3"),
                        MenuItem("Check environment", self.check_env, "4"),
                        MenuItem("Exit", self.exit_app, "q"),
                    ]
                )
                self.add_child(self.menu)
                
                self.app = None
            
            def new_project(self):
                """Create new project."""
                if self.app:
                    self.app.stop()
                print("\n")
                cmd_init()
                input("\nPress Enter to continue...")
            
            def run_project(self):
                """Run project."""
                if self.app:
                    self.app.stop()
                print("\n")
                cmd_run()
            
            def build_project(self):
                """Build project."""
                if self.app:
                    self.app.stop()
                print("\n")
                cmd_build()
                input("\nPress Enter to continue...")
            
            def check_env(self):
                """Check environment."""
                if self.app:
                    self.app.stop()
                print("\n")
                cmd_doctor()
                input("\nPress Enter to continue...")
            
            def exit_app(self):
                """Exit."""
                if self.app:
                    self.app.stop()
            
            def render(self, renderer):
                """Render screen."""
                for child in self.children:
                    child.render(renderer)
        
        # Create app
        screen = CLIScreen(Rect(1, 1, 80, 25))
        app = App(screen, inline=False, animated=False)
        screen.app = app
        
        # Apply theme
        theme = Themes.purple()  # Purple theme for CLI
        set_theme(theme)
        
        app.run()
        
    except ImportError:
        print("❌ KCM not installed!")
        print("Install KCM to use interactive mode.")
        return False
    
    return True


def show_help():
    """Show help message."""
    print("""
Usage: kcm [command] [arguments]

Commands:
  init <name>     Create new project
  run             Run current project
  build           Build project to exe/binary
  doctor          Check environment
  ui, menu        Interactive menu (default)
  help            Show this help

Examples:
  kcm                    # Interactive menu
  kcm init my_app        # Create project my_app
  kcm run                # Run app.py
  kcm build              # Build with Nuitka
  kcm doctor             # Check Python, Nuitka, KCM

Documentation: https://github.com/kasper-studios/kascmenu-engine
""")


def main():
    """Main CLI entry point."""
    # Interactive mode
    if INTERACTIVE:
        show_banner()
        show_interactive_menu()
        return
    
    # Command mode
    command = sys.argv[1]
    
    if command == "init":
        show_banner()
        if len(sys.argv) < 3:
            cmd_init()
        else:
            cmd_init(sys.argv[2])
    
    elif command == "run":
        show_banner()
        cmd_run()
    
    elif command == "build":
        show_banner()
        cmd_build()
    
    elif command == "doctor":
        show_banner()
        cmd_doctor()
    
    elif command in ["help", "--help", "-h"]:
        show_banner()
        show_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'kcm help' for help")
        sys.exit(1)


if __name__ == "__main__":
    main()

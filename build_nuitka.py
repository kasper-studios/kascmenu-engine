"""Build script for compiling KCM Chat with Nuitka - using KCM UI!"""
import subprocess
import sys
import platform
from kcmpy import App, Rect
from kcmpy.cui.menu import Menu, MenuItem
from kcmpy.cui.progress import StatusIndicator, Spinner
from kcmpy.cui.widgets import Box, Text
from kcmpy.core.component import Component
from kcmpy.core.theme import Themes, set_theme
import threading


class BuildScreen(Component):
    """Build screen with menu and status."""

    def __init__(self, rect):
        super().__init__(rect)
        
        # Title
        self.title = StatusIndicator(
            Rect(2, 2, rect.width - 4, 1),
            'info',
            '🔨 KCM Chat - Nuitka Build System'
        )
        self.add_child(self.title)
        
        # Menu
        self.menu = Menu(
            Rect(20, 5, 40, 12),
            title="Выберите действие",
            items=[
                MenuItem("Скомпилировать клиент", self.build_client, "1"),
                MenuItem("Скомпилировать сервер", self.build_server, "2"),
                MenuItem("Скомпилировать оба", self.build_both, "3"),
                MenuItem("Проверить Nuitka", self.check_nuitka, "4"),
                MenuItem("Выход", self.exit_app, "q"),
            ]
        )
        self.add_child(self.menu)
        
        # Status box
        self.status_box = Box(
            Rect(2, 18, rect.width - 4, 10),
            title="Статус",
            border_style='single'
        )
        self.add_child(self.status_box)
        
        # Status text
        self.status_text = Text(
            Rect(4, 20, rect.width - 8, 6),
            "Готов к компиляции.\nВыберите действие из меню выше."
        )
        self.status_box.add_child(self.status_text)
        
        # Spinner for building
        self.spinner = Spinner(Rect(4, 26, 30, 1), style='dots')
        self.spinner.visible = False
        self.status_box.add_child(self.spinner)
        
        self.building = False
        self.app = None

    def check_nuitka(self):
        """Check if Nuitka is installed."""
        self.status_text.text = "Проверка Nuitka и Cython..."
        
        # Check Python version
        python_version = sys.version_info
        needs_cython = python_version.major == 3 and python_version.minor >= 12
        
        # Check Nuitka
        try:
            result = subprocess.run(
                [sys.executable, "-m", "nuitka", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            version = result.stdout.strip()
            nuitka_status = f"✅ Nuitka установлен!\nВерсия: {version}"
        except (subprocess.CalledProcessError, FileNotFoundError):
            nuitka_status = "❌ Nuitka не установлен!\nУстановите: pip install nuitka"
        
        # Check Cython if needed
        cython_status = ""
        if needs_cython:
            try:
                import cython
                cython_version = cython.__version__
                cython_status = f"✅ Cython установлен!\nВерсия: {cython_version}"
            except ImportError:
                cython_status = "❌ Cython не установлен!\nДля Python 3.12+ требуется Cython!\nУстановите: pip install cython>=3.0.0"
        
        # Combine status
        status_lines = [nuitka_status]
        if needs_cython:
            status_lines.append(f"\nPython {python_version.major}.{python_version.minor} - требуется Cython")
            status_lines.append(cython_status)
        
        self.status_text.text = "\n\n".join(status_lines)

    def build_client(self):
        """Build chat client."""
        if self.building:
            return
        
        self.status_text.text = "🔨 Компиляция клиента...\n\nЭто может занять несколько минут.\nПожалуйста, подождите..."
        self.spinner.visible = True
        self.building = True
        
        def build():
            success = self._build_file(
                "chat_client_simple_notifications.py",
                "kcm_chat",
                ["kcmpy", "socketio"]
            )
            
            self.building = False
            self.spinner.visible = False
            
            if success:
                self.status_text.text = "✅ Клиент скомпилирован!\n\nФайл: dist/kcm_chat.exe\n(или dist/kcm_chat на Unix)"
            else:
                self.status_text.text = "❌ Ошибка компиляции клиента!\n\nПроверьте консоль для деталей."
        
        threading.Thread(target=build, daemon=True).start()

    def build_server(self):
        """Build chat server."""
        if self.building:
            return
        
        self.status_text.text = "🔨 Компиляция сервера...\n\nЭто может занять несколько минут.\nПожалуйста, подождите..."
        self.spinner.visible = True
        self.building = True
        
        def build():
            success = self._build_file(
                "chat_server.py",
                "kcm_chat_server",
                ["flask", "flask_socketio"]
            )
            
            self.building = False
            self.spinner.visible = False
            
            if success:
                self.status_text.text = "✅ Сервер скомпилирован!\n\nФайл: dist/kcm_chat_server.exe\n(или dist/kcm_chat_server на Unix)"
            else:
                self.status_text.text = "❌ Ошибка компиляции сервера!\n\nПроверьте консоль для деталей."
        
        threading.Thread(target=build, daemon=True).start()

    def build_both(self):
        """Build both client and server."""
        if self.building:
            return
        
        self.status_text.text = "🔨 Компиляция клиента и сервера...\n\nЭто займет 10-20 минут.\nПожалуйста, подождите..."
        self.spinner.visible = True
        self.building = True
        
        def build():
            # Build client
            success1 = self._build_file(
                "chat_client_simple_notifications.py",
                "kcm_chat",
                ["kcmpy", "socketio"]
            )
            
            if not success1:
                self.building = False
                self.spinner.visible = False
                self.status_text.text = "❌ Ошибка компиляции клиента!"
                return
            
            # Build server
            success2 = self._build_file(
                "chat_server.py",
                "kcm_chat_server",
                ["flask", "flask_socketio"]
            )
            
            self.building = False
            self.spinner.visible = False
            
            if success2:
                self.status_text.text = "✅ Оба файла скомпилированы!\n\nФайлы в dist/:\n- kcm_chat\n- kcm_chat_server"
            else:
                self.status_text.text = "❌ Ошибка компиляции сервера!\n\nКлиент скомпилирован успешно."
        
        threading.Thread(target=build, daemon=True).start()

    def _build_file(self, source: str, output: str, packages: list) -> bool:
        """Build a file with Nuitka."""
        is_windows = platform.system() == 'Windows'
        output_name = f"{output}.exe" if is_windows else output
        
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
        ]
        
        # Add packages
        for pkg in packages:
            cmd.append(f"--include-package={pkg}")
        
        # Exclude unnecessary
        cmd.extend([
            "--nofollow-import-to=tkinter",
            "--nofollow-import-to=matplotlib",
            "--nofollow-import-to=numpy",
        ])
        
        # Windows specific
        if is_windows:
            cmd.append("--windows-console-mode=attach")
        
        cmd.append(source)
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def exit_app(self):
        """Exit application."""
        if self.app:
            self.app.stop()

    def update(self, delta_time: float):
        """Update components."""
        if self.building:
            self.spinner.update(delta_time)
        super().update(delta_time)

    def render(self, renderer):
        """Render screen."""
        for child in self.children:
            child.render(renderer)


def main():
    """Run build UI."""
    print("=" * 70)
    print("  KCM Chat - Nuitka Build System")
    print("=" * 70)
    print("\nИспользуя KCM Framework для UI! 🎨")
    print("\nНажмите любую клавишу для начала...")
    input()
    
    # Create app
    screen = BuildScreen(Rect(1, 1, 80, 30))
    app = App(screen, inline=False, animated=True)
    screen.app = app
    
    # Apply theme
    theme = Themes.matrix()  # Хакерская тема для build системы 😎
    set_theme(theme)
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    
    print("\n" + "=" * 70)
    print("  Build System закрыт")
    print("=" * 70)
    print("\nИспользуйте build.bat (Windows) или build.sh (Unix)")
    print("для быстрой компиляции без UI.")


if __name__ == "__main__":
    main()

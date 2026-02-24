"""Input handling for keyboard and mouse events."""
import sys
import platform
from typing import Optional


class InputHandler:
    """Handle keyboard and mouse input in raw mode."""

    def __init__(self):
        self.old_settings = None
        self.is_windows = platform.system() == 'Windows'

    def __enter__(self):
        """Enter raw mode."""
        if not self.is_windows and sys.stdin.isatty():
            import termios
            import tty
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore terminal settings."""
        if not self.is_windows and self.old_settings:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_key(self, timeout: float = 0.0) -> Optional[str]:
        """Get a key press with optional timeout."""
        if self.is_windows:
            return self._get_key_windows(timeout)
        else:
            return self._get_key_unix(timeout)

    def _get_key_windows(self, timeout: float) -> Optional[str]:
        """Get key on Windows."""
        import msvcrt
        import time

        start_time = time.time()

        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()

                # Handle special keys
                if ch in (b'\x00', b'\xe0'):  # Special key prefix
                    ch2 = msvcrt.getch()
                    # Arrow keys
                    if ch2 == b'H':  # Up
                        return '\x1b[A'
                    elif ch2 == b'P':  # Down
                        return '\x1b[B'
                    elif ch2 == b'K':  # Left
                        return '\x1b[D'
                    elif ch2 == b'M':  # Right
                        return '\x1b[C'
                    return ch2.decode('utf-8', errors='ignore')

                # Handle multi-byte UTF-8 characters (Cyrillic, etc.)
                try:
                    # Try to decode as UTF-8
                    result = ch.decode('cp866', errors='ignore')  # Windows console uses cp866 for Cyrillic
                    if result:
                        return result

                    # If first byte indicates multi-byte UTF-8, read more bytes
                    if ch[0] >= 0xC0:  # Multi-byte UTF-8 start
                        bytes_to_read = 1
                        if ch[0] >= 0xE0:
                            bytes_to_read = 2
                        elif ch[0] >= 0xF0:
                            bytes_to_read = 3

                        # Read additional bytes
                        for _ in range(bytes_to_read):
                            if msvcrt.kbhit():
                                ch += msvcrt.getch()

                        return ch.decode('utf-8', errors='ignore')

                    return ch.decode('utf-8', errors='ignore')
                except (UnicodeDecodeError, AttributeError):
                    return None

            if timeout > 0 and (time.time() - start_time) >= timeout:
                return None

            time.sleep(0.001)

    def _get_key_unix(self, timeout: float) -> Optional[str]:
        """Get key on Unix/Linux."""
        import select
        
        if not sys.stdin.isatty():
            return None

        if select.select([sys.stdin], [], [], timeout)[0]:
            ch = sys.stdin.read(1)

            # Handle escape sequences
            if ch == '\x1b':
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch += sys.stdin.read(2)
            return ch
        return None

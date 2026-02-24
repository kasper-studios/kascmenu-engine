"""WebSocket chat client with simple console notifications (no win10toast)."""
import socketio
import threading
from datetime import datetime
from kcmpy import App, Rect
from kcmpy.core.screen import Screen, ScreenManager
from kcmpy.core.config import Config
from kcmpy.cui.input import TextInput, Button, Checkbox
from kcmpy.cui.widgets import Box
from kcmpy.cui.progress import StatusIndicator
from kcmpy.core.theme import Themes, set_theme
from kcmpy.events.event_system import EventType


class SimpleNotificationManager:
    """Simple notification manager without external dependencies."""

    def __init__(self):
        self.enabled = True
        self.notify_messages = True
        self.notify_joins = True
        self.notify_leaves = False
        self.notifications = []  # Store recent notifications
        self.max_notifications = 5

    def show(self, title: str, message: str):
        """Show notification in console."""
        if not self.enabled:
            return

        notification = f"[{datetime.now().strftime('%H:%M:%S')}] {title}: {message}"
        self.notifications.append(notification)
        
        # Keep only recent notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)

    def notify_new_message(self, username: str, message: str):
        """Notify about new message."""
        if self.enabled and self.notify_messages:
            preview = message[:30] + "..." if len(message) > 30 else message
            self.show("💬 Новое сообщение", f"{username}: {preview}")

    def notify_user_joined(self, username: str):
        """Notify about user joining."""
        if self.enabled and self.notify_joins:
            self.show("👋 Вход", f"{username} присоединился")

    def notify_user_left(self, username: str):
        """Notify about user leaving."""
        if self.enabled and self.notify_leaves:
            self.show("👋 Выход", f"{username} покинул чат")

    def get_recent_notifications(self):
        """Get recent notifications."""
        return self.notifications.copy()


class ChatMessage:
    """Chat message data."""

    def __init__(self, username: str, message: str, timestamp: str):
        self.username = username
        self.message = message
        self.timestamp = timestamp


class SettingsScreen(Screen):
    """Settings screen for server URL, nickname and notifications."""

    def __init__(self, rect, notification_manager, config):
        super().__init__(rect, "settings")
        self.notification_manager = notification_manager
        self.config = config

        # Load saved settings
        saved_url = config.get('server.url', 'http://localhost:5000')
        saved_nick = config.get('user.nickname', 'Пользователь')
        saved_notify_msg = config.get('notifications.messages', True)
        saved_notify_join = config.get('notifications.joins', True)
        saved_notify_leave = config.get('notifications.leaves', False)

        # Container
        self.box = Box(
            Rect(rect.x + 10, rect.y + 3, 60, 20),
            title="Настройки подключения",
            border_style='double'
        )
        self.add_child(self.box)

        # Server URL input
        self.url_input = TextInput(
            Rect(self.box.rect.x + 2, self.box.rect.y + 2, 56, 2),
            label="Адрес сервера:",
            placeholder="http://localhost:5000"
        )
        self.url_input.value = saved_url
        self.url_input.cursor_pos = len(self.url_input.value)
        self.box.add_child(self.url_input)

        # Nickname input
        self.nick_input = TextInput(
            Rect(self.box.rect.x + 2, self.box.rect.y + 6, 56, 2),
            label="Ваш никнейм:",
            placeholder="Аноним"
        )
        self.nick_input.value = saved_nick
        self.nick_input.cursor_pos = len(self.nick_input.value)
        self.box.add_child(self.nick_input)

        # Notification settings
        y_offset = 10
        self.notify_label = StatusIndicator(
            Rect(self.box.rect.x + 2, self.box.rect.y + y_offset, 56, 1),
            'info',
            'Настройки уведомлений (консольные):'
        )
        self.box.add_child(self.notify_label)

        self.notify_messages_cb = Checkbox(
            Rect(self.box.rect.x + 2, self.box.rect.y + y_offset + 1, 56, 1),
            "Уведомления о новых сообщениях",
            saved_notify_msg
        )
        self.notification_manager.notify_messages = saved_notify_msg
        self.notify_messages_cb.on_change = self._on_notify_messages_change
        self.box.add_child(self.notify_messages_cb)

        self.notify_joins_cb = Checkbox(
            Rect(self.box.rect.x + 2, self.box.rect.y + y_offset + 2, 56, 1),
            "Уведомления о входе пользователей",
            saved_notify_join
        )
        self.notification_manager.notify_joins = saved_notify_join
        self.notify_joins_cb.on_change = self._on_notify_joins_change
        self.box.add_child(self.notify_joins_cb)

        self.notify_leaves_cb = Checkbox(
            Rect(self.box.rect.x + 2, self.box.rect.y + y_offset + 3, 56, 1),
            "Уведомления о выходе пользователей",
            saved_notify_leave
        )
        self.notification_manager.notify_leaves = saved_notify_leave
        self.notify_leaves_cb.on_change = self._on_notify_leaves_change
        self.box.add_child(self.notify_leaves_cb)

        # Connect button
        self.connect_btn = Button(
            Rect(self.box.rect.x + 20, self.box.rect.y + 16, 20, 1),
            "Подключиться",
            self.connect
        )
        self.box.add_child(self.connect_btn)

        # Status
        self.status = StatusIndicator(
            Rect(self.box.rect.x + 2, self.box.rect.y + 18, 56, 1),
            'success',
            'Настройки загружены из ~/.kcm/kcm_chat.json'
        )
        self.box.add_child(self.status)

        # Focus management
        self.focusable = [
            self.url_input,
            self.nick_input,
            self.notify_messages_cb,
            self.notify_joins_cb,
            self.notify_leaves_cb,
            self.connect_btn
        ]
        self.focused_index = 0
        self.focusable[0].focused = True

    def _on_notify_messages_change(self, checked):
        """Handle notify messages checkbox change."""
        self.notification_manager.notify_messages = checked
        self.config.set('notifications.messages', checked)
        self.config.save()

    def _on_notify_joins_change(self, checked):
        """Handle notify joins checkbox change."""
        self.notification_manager.notify_joins = checked
        self.config.set('notifications.joins', checked)
        self.config.save()

    def _on_notify_leaves_change(self, checked):
        """Handle notify leaves checkbox change."""
        self.notification_manager.notify_leaves = checked
        self.config.set('notifications.leaves', checked)
        self.config.save()

    def connect(self):
        """Connect to chat server."""
        url = self.url_input.value.strip() or "http://localhost:5000"
        nickname = self.nick_input.value.strip() or "Аноним"

        # Save settings
        self.config.set('server.url', url)
        self.config.set('user.nickname', nickname)
        self.config.save()

        # Pass to chat screen
        chat_screen = self.screen_manager.screens.get("chat")
        if chat_screen:
            chat_screen.connect(url, nickname)
            self.screen_manager.switch_to("chat")

    def handle_event(self, event):
        """Handle events."""
        if event.type == EventType.KEY_PRESS:
            key = event.data.get('key', '')

            # Tab to switch focus
            if key == '\t':
                self.focusable[self.focused_index].focused = False
                self.focused_index = (self.focused_index + 1) % len(self.focusable)
                self.focusable[self.focused_index].focused = True
                return True

            # Enter on button
            if key in ('\r', '\n') and self.focused_index == len(self.focusable) - 1:
                self.connect()
                return True

        return self.focusable[self.focused_index].handle_event(event)

    def render(self, renderer):
        """Render screen."""
        self.box.render(renderer)


class ChatScreen(Screen):
    """Main chat screen with simple notifications."""

    def __init__(self, rect, notification_manager):
        super().__init__(rect, "chat")

        self.sio = socketio.Client()
        self.connected = False
        self.messages = []
        self.server_url = ""
        self.nickname = ""
        self.scroll_offset = 0
        self.needs_render = False
        self.notification_manager = notification_manager

        # Setup SocketIO handlers
        self.setup_socketio()

        # Header
        self.header = StatusIndicator(
            Rect(2, 2, rect.width - 4, 1),
            'info',
            'Чат KCM - Отключен'
        )
        self.add_child(self.header)

        # Messages box
        self.msg_box = Box(
            Rect(2, 4, rect.width - 4, rect.height - 10),
            title="Сообщения",
            border_style='single'
        )
        self.add_child(self.msg_box)

        # Input field
        self.input_field = TextInput(
            Rect(2, rect.height - 4, rect.width - 4, 2),
            label="Сообщение:",
            placeholder="Введите сообщение..."
        )
        self.input_field.focused = True
        self.add_child(self.input_field)

        # Status bar
        self.status = StatusIndicator(
            Rect(2, rect.height - 1, rect.width - 4, 1),
            'info',
            'Enter - отправить | Esc - настройки | q - выход | 🔔 Консольные уведомления'
        )
        self.add_child(self.status)

    def setup_socketio(self):
        """Setup SocketIO event handlers."""

        @self.sio.on('connect')
        def on_connect():
            self.connected = True
            self.header.status = 'success'
            self.header.message = f'Чат KCM - Подключен как {self.nickname}'
            self.needs_render = True
            # Send join event
            self.sio.emit('join', {'username': self.nickname})

        @self.sio.on('disconnect')
        def on_disconnect():
            self.connected = False
            self.header.status = 'error'
            self.header.message = 'Чат KCM - Отключен'
            self.needs_render = True

        @self.sio.on('message')
        def on_message(data):
            username = data.get('username', 'Unknown')
            message = data.get('message', '')
            timestamp = data.get('timestamp', '')

            msg = ChatMessage(username, message, timestamp)
            self.messages.append(msg)

            # Show notification if not from self
            if username != self.nickname:
                self.notification_manager.notify_new_message(username, message)

            # Auto-scroll to bottom
            self.scroll_offset = max(0, len(self.messages) - self.get_visible_lines())
            self.needs_render = True

        @self.sio.on('user_joined')
        def on_user_joined(data):
            username = data.get('username', 'Unknown')
            msg = ChatMessage('System', f'{username} присоединился к чату', datetime.now().strftime('%H:%M:%S'))
            self.messages.append(msg)

            # Show notification if not self
            if username != self.nickname:
                self.notification_manager.notify_user_joined(username)

            self.scroll_offset = max(0, len(self.messages) - self.get_visible_lines())
            self.needs_render = True

        @self.sio.on('user_left')
        def on_user_left(data):
            username = data.get('username', 'Unknown')
            msg = ChatMessage('System', f'{username} покинул чат', datetime.now().strftime('%H:%M:%S'))
            self.messages.append(msg)

            # Show notification
            self.notification_manager.notify_user_left(username)

            self.scroll_offset = max(0, len(self.messages) - self.get_visible_lines())
            self.needs_render = True

        @self.sio.on('history')
        def on_history(data):
            history = data.get('messages', [])
            for msg_data in history:
                msg = ChatMessage(
                    msg_data.get('username', 'Unknown'),
                    msg_data.get('message', ''),
                    msg_data.get('timestamp', '')
                )
                self.messages.append(msg)
            self.scroll_offset = max(0, len(self.messages) - self.get_visible_lines())
            self.needs_render = True

    def connect(self, url: str, nickname: str):
        """Connect to server."""
        self.server_url = url
        self.nickname = nickname
        self.messages.clear()

        # Show connecting status
        self.header.status = 'warning'
        self.header.message = f'Чат KCM - Подключение к {url}...'
        self.needs_render = True

        # Connect in background thread
        def connect_thread():
            try:
                self.sio.connect(url)
            except Exception as e:
                msg = ChatMessage('System', f'Ошибка подключения: {str(e)}', datetime.now().strftime('%H:%M:%S'))
                self.messages.append(msg)
                self.header.status = 'error'
                self.header.message = 'Чат KCM - Ошибка подключения'
                self.needs_render = True

        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()

    def disconnect(self):
        """Disconnect from server."""
        if self.connected:
            self.sio.disconnect()

    def send_message(self):
        """Send message to server."""
        message = self.input_field.value.strip()
        if not message or not self.connected:
            return

        self.sio.emit('message', {'message': message})
        self.input_field.value = ""
        self.input_field.cursor_pos = 0
        self.needs_render = True

    def update(self, delta_time: float):
        """Update screen state."""
        super().update(delta_time)
        # Check if we need to re-render due to incoming messages
        if self.needs_render:
            self.needs_render = False
            # Clear screen for clean render
            if self.screen_manager and self.screen_manager.app:
                self.screen_manager.app._clear_screen()
            return True
        return False

    def get_visible_lines(self) -> int:
        """Get number of visible message lines."""
        return self.msg_box.rect.height - 2

    def handle_event(self, event):
        """Handle events."""
        if event.type == EventType.KEY_PRESS:
            key = event.data.get('key', '')

            # Send message
            if key in ('\r', '\n'):
                self.send_message()
                return True

            # Scroll up
            elif key == '\x1b[A':  # Up arrow
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1
                return True

            # Scroll down
            elif key == '\x1b[B':  # Down arrow
                max_scroll = max(0, len(self.messages) - self.get_visible_lines())
                if self.scroll_offset < max_scroll:
                    self.scroll_offset += 1
                return True

            # Back to settings
            elif key == '\x1b':  # Esc
                self.disconnect()
                self.screen_manager.switch_to("settings")
                return True

        return self.input_field.handle_event(event)

    def render(self, renderer):
        """Render screen."""
        # Render header
        self.header.render(renderer)

        # Render message box
        self.msg_box.render(renderer)

        # Render messages
        visible_lines = self.get_visible_lines()
        start_idx = self.scroll_offset
        end_idx = min(start_idx + visible_lines, len(self.messages))

        y = self.msg_box.rect.y + 1
        max_width = self.msg_box.rect.width - 4  # Учитываем отступы
        
        for i in range(start_idx, end_idx):
            if y >= self.msg_box.rect.y + self.msg_box.rect.height - 1:
                break  # Не выходим за границы
                
            msg = self.messages[i]
            renderer.move_cursor(self.msg_box.rect.x + 2, y)

            # Format message
            if msg.username == 'System':
                from kcmpy.core.renderer import Style
                style = Style(fg='bright_black', italic=True)
                text = f"[{msg.timestamp}] {msg.message}"
                # Обрезаем если слишком длинное
                if len(text) > max_width:
                    text = text[:max_width-3] + "..."
                renderer.buffer.append(renderer.style_text(text, style))
            else:
                from kcmpy.core.renderer import Style
                style_user = Style(fg='bright_cyan', bold=True)
                style_msg = Style(fg='white')
                style_time = Style(fg='bright_black')

                # Формируем префикс
                prefix = f"[{msg.timestamp}] {msg.username}: "
                prefix_len = len(prefix)
                
                # Обрезаем сообщение если нужно
                message_text = msg.message
                available_width = max_width - prefix_len
                if len(message_text) > available_width:
                    message_text = message_text[:available_width-3] + "..."
                
                renderer.buffer.append(renderer.style_text(f"[{msg.timestamp}] ", style_time))
                renderer.buffer.append(renderer.style_text(f"{msg.username}: ", style_user))
                renderer.buffer.append(renderer.style_text(message_text, style_msg))
            
            y += 1

        # Render input field
        self.input_field.render(renderer)

        # Render status bar
        self.status.render(renderer)


def main():
    """Run chat client with simple notifications."""
    print("=" * 70)
    print("  KCM Chat Client с консольными уведомлениями")
    print("=" * 70)
    print("\nВозможности:")
    print("  • WebSocket подключение к серверу")
    print("  • Настройка адреса сервера и никнейма")
    print("  • 📝 Консольные уведомления (без win10toast)")
    print("  • Настройка типов уведомлений")
    print("  • Прокрутка истории сообщений")
    print("  • 💾 Автосохранение настроек в ~/.kcm/kcm_chat.json")
    print("\n💡 Эта версия не требует win10toast")
    print("\nНажмите любую клавишу для начала...")
    input()

    # Create config
    config = Config(app_name="kcm_chat")

    # Create notification manager
    notification_manager = SimpleNotificationManager()

    # Create app
    from kcmpy.core.component import Component
    app = App(Component(Rect(1, 1, 80, 30)), inline=False, animated=False)

    # Create screen manager
    screens = ScreenManager(app)
    app.screens = screens

    # Create screens
    settings_screen = SettingsScreen(Rect(1, 1, 80, 30), notification_manager, config)
    chat_screen = ChatScreen(Rect(1, 1, 80, 30), notification_manager)

    screens.add_screen("settings", settings_screen)
    screens.add_screen("chat", chat_screen)

    # Start with settings
    screens.switch_to("settings")

    # Apply theme
    theme = Themes.default()
    set_theme(theme)

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        if chat_screen.connected:
            chat_screen.disconnect()
        
        # Show notifications summary
        notifications = notification_manager.get_recent_notifications()
        if notifications:
            print("\n" + "=" * 70)
            print("  Последние уведомления:")
            print("=" * 70)
            for notif in notifications:
                print(notif)
        
        # Show config location
        print(f"\n💾 Настройки сохранены в: {config.config_file}")

    print("\nСпасибо за использование KCM Chat!")


if __name__ == "__main__":
    main()

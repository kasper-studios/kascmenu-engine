# KCM Chat Client (JavaScript)

WebSocket chat client built with KCM framework for Node.js.

## Features

- 🌐 WebSocket connection to chat server
- ⚙️ Configurable server URL and nickname
- 📝 Console notifications for messages and user events
- 🔔 Customizable notification settings
- 📜 Message history with scrolling
- 💾 Auto-save settings to `~/.kcm/kcm_chat.json`
- 🌍 Unicode/Cyrillic support

## Installation

```bash
cd kcmjs
npm install
```

## Usage

1. Start the chat server (from project root):
```bash
python chat_server.py
```

2. Run the chat client:
```bash
npm run chat
# or
node chat_client.js
```

## Controls

### Settings Screen
- `Tab` - Switch between input fields
- `Space` - Toggle checkboxes
- `Enter` - Connect to server

### Chat Screen
- `Enter` - Send message
- `↑/↓` - Scroll message history
- `Esc` - Back to settings
- `q` - Quit

## Configuration

Settings are automatically saved to `~/.kcm/kcm_chat.json`:

```json
{
  "server": {
    "url": "http://localhost:5000"
  },
  "user": {
    "nickname": "User"
  },
  "notifications": {
    "messages": true,
    "joins": true,
    "leaves": false
  }
}
```

## Architecture

The chat client uses the same architecture as the Python version:

- `SimpleNotificationManager` - Console-based notifications
- `Config` - Settings persistence
- `SettingsScreen` - Connection configuration UI
- `ChatScreen` - Main chat interface with message display
- `ChatApp` - Application coordinator

## Dependencies

- `socket.io-client` - WebSocket client library

## Notes

This is a direct port of the Python chat client (`chat_client_simple_notifications.py`) to JavaScript, maintaining the same features and user experience.

## Comparison with Python Version

| Feature | Python | JavaScript |
|---------|--------|------------|
| WebSocket | ✅ | ✅ |
| Settings UI | ✅ | ✅ |
| Message History | ✅ | ✅ |
| Scrolling | ✅ | ✅ |
| Notifications | ✅ | ✅ |
| Config Persistence | ✅ | ✅ |
| Unicode Support | ✅ | ✅ |
| Alternate Screen Buffer | ✅ | ✅ |

Both versions provide identical functionality and user experience.

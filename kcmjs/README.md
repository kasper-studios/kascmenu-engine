# KCM.js - Console User Interface Framework for Node.js

Modern framework for creating Console User Interfaces in JavaScript/Node.js.

## 📦 Installation

```bash
npm install
```

## 🎨 Features

### Core Components
- **App** - Main application with event-driven rendering
- **Component** - Base class for all UI elements
- **Renderer** - ANSI terminal rendering with buffering
- **EventBus** - Event system for component communication

### Widgets
- **Box, Text** - Containers and text blocks
- **Menu, MenuItem** - Interactive menus with keyboard navigation
- **SelectList** - Selectable list with multi-select support
- **ProgressBar** - Progress bar with percentage
- **Spinner** - Animated loading spinner (10+ styles)
- **MultiProgressBar** - Multiple progress bars
- **StatusIndicator** - Status with icons ([OK], [X], [!], [i])
- **TextInput** - Text input field with cursor and Unicode support
- **Checkbox** - Checkbox with callback
- **RadioGroup** - Radio button group
- **Button** - Clickable button with styling

### Key Features
- ✅ Event-driven architecture (no constant FPS loop)
- ✅ ANSI color and style support
- ✅ Keyboard input handling
- ✅ Focus management
- ✅ Unicode/Cyrillic support
- ✅ Alternate screen buffer (like nano/vim)
- ✅ Cross-platform (Windows/Unix)

## 🚀 Quick Start

### Simple Menu Example

```javascript
import { App } from './core/app.js';
import { Rect } from './core/component.js';
import { Menu, MenuItem } from './cui/menu.js';

const menu = new Menu(
    new Rect(10, 5, 40, 8),
    {
        title: 'Main Menu',
        items: [
            new MenuItem('New Project', () => console.log('Created!'), 'n'),
            new MenuItem('Open Project', () => console.log('Opened!'), 'o'),
            new MenuItem('Exit', () => process.exit(0), 'q')
        ]
    }
);

const app = new App(menu, { inline: false, animated: false });
app.run();
```

### Widget Demo

```javascript
import { App } from './core/app.js';
import { Component, Rect } from './core/component.js';
import { ProgressBar, Spinner, StatusIndicator } from './cui/progress.js';
import { TextInput, Button } from './cui/input.js';

const root = new Component(new Rect(1, 1, 80, 30));

// Add widgets
const progress = new ProgressBar(new Rect(5, 5, 40, 1));
progress.setProgress(75);
root.addChild(progress);

const spinner = new Spinner(new Rect(5, 7, 40, 1), { style: 'dots', text: 'Loading...' });
root.addChild(spinner);

const status = new StatusIndicator(new Rect(5, 9, 40, 1), 'success', 'Operation completed');
root.addChild(status);

const input = new TextInput(new Rect(5, 11, 40, 2), { label: 'Name:', placeholder: 'Enter name' });
input.focused = true;
root.addChild(input);

const app = new App(root, { inline: false, animated: true });
app.run();
```

## 📚 Examples

Run examples:
```bash
npm run example        # Basic demo
npm run example:menu   # Menu demo
npm run example:widgets # All widgets demo
npm run chat           # WebSocket chat client
```

## 💬 WebSocket Chat Client

Full-featured chat client with:
- Server URL and nickname configuration
- Real-time messaging
- Message history with scrolling
- Console notifications
- Settings persistence to `~/.kcm/kcm_chat.json`

### Usage

1. Start the Python chat server (from project root):
```bash
python chat_server.py
```

2. Run the chat client:
```bash
npm run chat
```

See [CHAT_README.md](CHAT_README.md) for details.

## 🎮 Controls

- `q` - Exit application
- `Tab` - Switch focus between elements
- `↑/↓` - Navigate menus/lists
- `Space/Enter` - Select/activate
- `Backspace` - Delete character in text input
- `←/→` - Move cursor in text input

## 📝 API Overview

### App
```javascript
const app = new App(rootComponent, options);
app.run();
app.stop();
```

Options:
- `inline` - Render inline (true) or fullscreen (false)
- `animated` - Enable animation loop for dynamic updates

### Component
```javascript
class MyComponent extends Component {
    constructor(rect) {
        super(rect);
    }
    
    render(renderer) {
        // Render logic
    }
    
    handleKey(key) {
        // Handle keyboard input
        return true; // if handled
    }
    
    update(deltaTime) {
        // Update state
    }
}
```

### Renderer
```javascript
renderer.moveCursor(x, y);
renderer.buffer.push(renderer.styleText(text, style));
renderer.render(); // Flush buffer to terminal
```

### Style
```javascript
import { Style } from './core/renderer.js';

const style = new Style({
    fg: 'brightCyan',
    bg: 'black',
    bold: true,
    italic: false,
    underline: false
});
```

## 🎨 Color Reference

Foreground/Background colors:
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- `brightBlack`, `brightRed`, `brightGreen`, `brightYellow`, `brightBlue`, `brightMagenta`, `brightCyan`, `brightWhite`

## 📦 Package Info

- **Name:** kascmpy
- **Version:** 0.1.0
- **License:** MIT
- **Author:** kasperenok <kasperstudioshelp@gmail.com>
- **Repository:** https://github.com/kasper-studios/kascmenu-engine

## 🔗 Related

- Python version: See main [README.md](../README.md)
- Architecture: [ARCHITECTURE.md](../ARCHITECTURE.md)
- Examples: [EXAMPLES.md](../EXAMPLES.md)

## 📝 License

MIT

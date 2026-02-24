# KCM Framework - Architecture and Roadmap

## Current State (v0.1)

### ✅ What Works

#### Core Layer
- **Component** - base class for all UI elements
- **Renderer** - ANSI rendering with cross-platform support
- **App** - main loop with event-driven architecture
- **InputHandler** - keyboard handling (including Unicode/Cyrillic)
- **EventBus** - event system

#### Screen Management
- **Screen** - base class for screens
- **ScreenManager** - routing between screens
- **Dialog** - modal windows (MessageDialog, ConfirmDialog)
- Lifecycle hooks: on_enter, on_exit, on_pause, on_resume

#### Widgets
- **Containers**: Box, Text
- **Menus**: Menu, MenuItem, SelectList
- **Progress**: ProgressBar, Spinner, MultiProgressBar, StatusIndicator
- **Input**: TextInput, Checkbox, RadioGroup, Button
- **Data**: Table, Chart, TreeView

#### Layout System
- **VBox** - vertical layout
- **HBox** - horizontal layout
- **Grid** - grid
- **Stack** - z-index layers
- **Anchor** - positioning

#### Styling
- **Style** - colors, bold, italic, underline
- **Theme** - 7 preset themes
- **WidgetStyle** - padding, margin, border, shadow
- **StyledWidget** - mixin for styling

#### Advanced Features
- **needs_render** - dirty flag system
- **animated mode** - for animated widgets
- **focus system** - Tab navigation
- **async updates** - WebSocket and threading support

### 🎯 Proven Use Cases

1. **Simple Menu** - quick menu for CLI tools
2. **Widget Showcase** - demo of all widgets with animation
3. **Multi-screen App** - navigation between screens
4. **WebSocket Chat** - real application with:
   - Settings UI
   - Real-time communication
   - Push notifications
   - System integration

## 🔧 Architectural Decisions

### 1. Event-driven Rendering
```python
# Don't spam render constantly
if self.needs_render:
    self.needs_render = False
    return True
```

**Advantages:**
- CPU efficient
- Smooth operation
- Supports async updates

### 2. Component-based Architecture
```python
class MyScreen(Screen):
    def __init__(self, rect):
        super().__init__(rect)
        self.add_child(widget1)
        self.add_child(widget2)
```

**Advantages:**
- Composition over inheritance
- Component reusability
- Logic isolation

### 3. Screen Manager as Router
```python
screens.add_screen("settings", settings_screen)
screens.add_screen("chat", chat_screen)
screens.switch_to("chat")
```

**Advantages:**
- Explicit transitions
- Lifecycle management
- Modal windows via push/pop

### 4. Dirty Flag Optimization
```python
@self.sio.on('message')
def on_message(data):
    self.messages.append(msg)
    self.needs_render = True  # Trigger redraw
```

**Advantages:**
- Render only on changes
- Works with async data sources
- Non-blocking UI

## ⚠️ Known Limitations

### 1. Thread Safety
**Problem:**
```python
# WebSocket callbacks mutate state from different thread
self.messages.append(msg)
self.header.status = 'success'
```

**Future Solution:**
```python
# Event queue
app.post_event(lambda: self.messages.append(msg))
```

### 2. Manual Render in Screen
**Current:**
```python
def render(self, renderer):
    self.header.render(renderer)
    self.msg_box.render(renderer)
    self.input_field.render(renderer)
```

**Could be:**
```python
def render(self, renderer):
    super().render(renderer)  # Renders children
    self.render_custom_content(renderer)
```

### 3. No Screen Templates
**Current:** each screen is written from scratch

**Future:**
```python
class SettingsScreen(FormScreen):
    fields = [
        TextField("url", "Server URL"),
        TextField("nickname", "Nickname"),
        CheckboxField("notify", "Notifications")
    ]
```

## 🚀 Roadmap

### v0.2 - Stabilization
- [ ] Thread-safe event queue
- [ ] Base Screen.render() for children
- [ ] API Documentation
- [ ] Unit tests for core components
- [ ] Examples for each widget

### v0.3 - Template Screens
- [ ] FormScreen - automatic forms
- [ ] ListScreen - lists with navigation
- [ ] LogScreen - logs with auto-scroll
- [ ] WizardScreen - multi-step wizards
- [ ] SplitScreen - split screen layout

### v0.4 - Advanced Widgets
- [ ] DatePicker - date selection
- [ ] ColorPicker - color selection
- [ ] FileExplorer - file browser
- [ ] CodeEditor - syntax highlighting editor
- [ ] Terminal - embedded terminal

### v0.5 - Developer Experience
- [ ] Hot reload for development
- [ ] Debug mode with component borders
- [ ] Performance profiler
- [ ] Component inspector
- [ ] CLI for project generation

### v1.0 - Production Ready
- [ ] Complete Documentation
- [ ] Tutorials and guides
- [ ] Stable API
- [ ] Real-world application examples
- [ ] Package on PyPI

## 💡 Future Ideas

### 1. Declarative Syntax
```python
@screen
def settings_screen():
    with VBox():
        Text("Settings")
        input_url = TextInput("URL")
        input_nick = TextInput("Nickname")
        Button("Connect", on_click=connect)
```

### 2. Reactive State
```python
class ChatScreen(Screen):
    messages = State([])  # Auto-render on change

    def add_message(self, msg):
        self.messages.append(msg)  # Triggers render
```

### 3. Middleware System
```python
app.use(LoggingMiddleware())
app.use(AuthMiddleware())
app.use(ThemeMiddleware())
```

### 4. Plugin System
```python
app.register_plugin(NotificationPlugin())
app.register_plugin(DatabasePlugin())
```

### 5. Bindings for Other Languages
- JavaScript (foundation exists)
- Rust
- Go
- C#

## 📊 Quality Metrics

### Code Coverage
- [ ] Core: 80%+
- [ ] Widgets: 70%+
- [ ] Screens: 60%+

### Performance
- [ ] Render < 16ms (60 FPS)
- [ ] Input latency < 50ms
- [ ] Memory leak free

### Developer Experience
- [ ] Simple menu creation time: < 5 minutes
- [ ] Multi-screen app creation time: < 30 minutes
- [ ] Documentation covers 90% of use cases

## 🎓 Lessons Learned

### What Worked Well
1. **Event-driven instead of FPS loop** - CPU efficient
2. **Component composition** - flexibility and reusability
3. **Screen Manager** - clean navigation
4. **Dirty flags** - render optimization
5. **Cross-platform from day one** - less pain later

### What Could Be Better
1. **Thread safety** - should have implemented event queue from the start
2. **Testing** - should write tests alongside code
3. **Documentation** - should document API immediately
4. **Examples** - need more examples for each widget

### What Was Surprising
1. **Unicode/Cyrillic** - more complex than expected (cp866 on Windows)
2. **Notifications** - easy to integrate
3. **WebSocket** - works great with event-driven architecture
4. **Development speed** - real application built in short time

## 🤝 Contributing

### Priorities
1. **Stability** > new features
2. **Documentation** > code
3. **Examples** > abstractions
4. **Simplicity** > "cleverness"

### Code Style
- Type hints everywhere
- Docstrings for public methods
- Examples in docstrings
- Tests for new features

## 📝 Conclusion

KCM Framework has already proven its viability:
- ✅ Architecture scales well
- ✅ API is intuitive
- ✅ Performance is sufficient
- ✅ Real use cases work

Next step - stabilization and templates for faster development.

---

**Version:** 0.1.0
**Date:** 2026-02-24
**Status:** Active Development

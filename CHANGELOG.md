# Changelog

Все значимые изменения в проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
версионирование следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `chat_client_simple_notifications.py` - версия с консольными уведомлениями (без win10toast)
- `CHAT_VERSIONS.md` - гайд по выбору версии клиента
- `kcmpy/core/config.py` - система сохранения настроек в JSON
- `build_nuitka.py` - интерактивная build система с KCM UI! 🎨
- `build.bat` / `build.sh` - быстрые скрипты компиляции
- `BUILD_GUIDE.md` - полное руководство по компиляции с Nuitka
- **`kcm_cli.py` - CLI инструмент для scaffolding проектов!** 🛠️
- **`kcm` / `kcm.bat` - wrapper скрипты для удобного запуска**
- **`CLI_GUIDE.md` - полное руководство по KCM CLI**
- **Автосохранение настроек** в `~/.kcm/kcm_chat.json`
- **Интерактивный режим CLI** - меню на KCM UI (dogfooding!)
- **Команды**: `init`, `run`, `build`, `doctor`

### Fixed
- Проблема с рендерингом в чате (артефакты и наложение текста)
- Ошибка win10toast `WNDPROC return value cannot be converted to LRESULT`
- Экран теперь очищается при обновлениях в ChatScreen
- Улучшена обработка ошибок в NotificationManager
- **Длинные сообщения теперь обрезаются с "..." вместо выхода за границы**
- Сообщения не ломают рамку чата

### Changed
- `chat_client_notifications.py` - улучшена обработка ошибок win10toast
- Рекомендуется использовать `chat_client_simple_notifications.py` для стабильности
- Рендеринг сообщений учитывает ширину окна и обрезает длинные строки
- **build_nuitka.py теперь использует KCM UI** - демонстрация возможностей фреймворка!
- **KCM CLI использует KCM для своего UI** - ultimate dogfooding! 🎨

### Planned
- Thread-safe event queue
- Template screens (FormScreen, ListScreen, LogScreen)
- Unit tests для core компонентов
- API documentation
- Hot reload для разработки

## [0.1.0] - 2026-02-24

### Added - Core Framework
- **Component** - базовый класс для всех UI элементов
- **Renderer** - ANSI рендеринг с кроссплатформенностью
- **App** - главный цикл с event-driven архитектурой
- **InputHandler** - обработка клавиатуры с поддержкой Unicode/кириллицы
- **EventBus** - система событий (KEY_PRESS, MOUSE_CLICK, etc.)

### Added - Screen Management
- **Screen** - базовый класс для экранов
- **ScreenManager** - роутинг между экранами (switch_to, push, pop)
- **Dialog** - модальные окна (MessageDialog, ConfirmDialog)
- Lifecycle hooks: on_enter, on_exit, on_pause, on_resume

### Added - Widgets (20+)
- **Containers**: Box, Text
- **Menus**: Menu, MenuItem, SelectList
- **Progress**: ProgressBar, Spinner (10+ стилей), MultiProgressBar, StatusIndicator
- **Input**: TextInput, Checkbox, RadioGroup, Button
- **Data**: Table, Chart, TreeView

### Added - Layout System
- **VBox** - вертикальная компоновка с фиксированными/гибкими высотами
- **HBox** - горизонтальная компоновка с фиксированными/гибкими ширинами
- **Grid** - сетка rows x cols с spanning
- **Stack** - z-index слои
- **Anchor** - позиционирование относительно краев

### Added - Styling & Themes
- **Style** - цвета, bold, italic, underline
- **Theme** - система тем с 7 предустановленными (Default, Dark, Light, Purple, Matrix, Ocean, Fire)
- **WidgetStyle** - padding, margin, border (6 стилей), shadow
- **StyledWidget** - миксин для применения стилей
- Автоматический выбор ASCII/Unicode символов по платформе

### Added - Advanced Features
- **needs_render** - dirty flag система для оптимизации
- **animated mode** - режим для виджетов с анимацией
- **focus system** - Tab навигация между элементами
- **async updates** - поддержка WebSocket и threading
- **Unicode/Cyrillic** - полная поддержка кириллицы на Windows (cp866) и Linux (UTF-8)

### Added - Examples
- `example.py` - простое меню
- `example_menu.py` - интерактивное меню с быстрыми клавишами
- `example_widgets.py` - демо всех виджетов с анимацией
- `example_screens.py` - multi-screen приложение с VBox/HBox/Grid
- `example_themes.py` - демонстрация всех тем
- `test_cyrillic_input.py` - тест ввода кириллицы

### Added - Real-world Application: WebSocket Chat
- `chat_server.py` - Flask-SocketIO сервер с веб-интерфейсом
- `chat_client.py` - базовый CUI клиент чата
- `chat_client_notifications.py` - клиент с push-уведомлениями
- **Features**:
  - Настройка сервера и никнейма через UI
  - Real-time сообщения через WebSocket
  - История сообщений с прокруткой
  - Уведомления о входе/выходе пользователей
  - Push-уведомления (Windows Toast, Linux notify-send)
  - Настройка типов уведомлений через чекбоксы

### Added - Documentation
- `README.md` - обзор проекта
- `ARCHITECTURE.md` - архитектура, roadmap, lessons learned
- `EXAMPLES.md` - примеры кода для всех use cases
- `PROJECT_SUMMARY.md` - краткое резюме проекта
- `QUICKSTART_CHAT.md` - быстрый старт чата
- `NOTIFICATIONS_GUIDE.md` - гайд по уведомлениям
- `TEST_NOTIFICATIONS.md` - тестирование уведомлений
- `test_chat.md` - инструкция по тестированию чата

### Fixed
- Рендеринг без спама (event-driven вместо 60 FPS loop)
- Артефакты при переходах между экранами (добавлен clear_screen)
- Фантомные строки от виджетов (убраны `\n` из render методов)
- Проблемы с фокусом (добавлена система focused/focusable)
- Автоматическое обновление при WebSocket событиях (needs_render флаг)
- Ввод кириллицы на Windows (поддержка cp866 и многобайтовых символов)
- Обработка Unicode символов в TextInput

### Changed
- Component.render() из abstract в concrete с дефолтной реализацией
- App.run() теперь периодически проверяет updates даже в не-анимированном режиме
- InputHandler читает многобайтовые UTF-8 символы на Windows
- TextInput принимает все Unicode символы кроме control-символов

### Technical Details
- **Lines of Code**: ~6000 (Python + examples + docs)
- **Widgets**: 20+
- **Themes**: 7
- **Examples**: 8
- **Documentation**: 7 файлов

### Performance
- Event-driven рендеринг экономит CPU
- Dirty flags минимизируют перерисовки
- Async updates не блокируют UI
- Рендер < 16ms для 60 FPS

### Platform Support
- ✅ Windows 10/11 (cmd, PowerShell, Windows Terminal)
- ✅ Linux (bash, zsh, любой ANSI терминал)
- ✅ macOS (Terminal.app, iTerm2)

### Dependencies
- Python 3.7+
- flask >= 3.0.0 (для chat_server)
- flask-socketio >= 5.3.0 (для chat_server)
- python-socketio >= 5.11.0 (для chat_client)
- win10toast >= 0.9 (опционально, для уведомлений на Windows)

## [0.0.1] - 2026-02-23

### Added
- Начальная версия проекта
- Базовая структура фреймворка
- Простое меню

---

## Типы изменений

- **Added** - новые фичи
- **Changed** - изменения в существующем функционале
- **Deprecated** - функционал который скоро будет удален
- **Removed** - удаленный функционал
- **Fixed** - исправления багов
- **Security** - исправления уязвимостей

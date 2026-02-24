# KCM Chat - Руководство по компиляции

## 🎯 Зачем компилировать?

Компиляция с Nuitka создает standalone исполняемые файлы:
- ✅ Не нужен Python на целевой машине
- ✅ Один файл вместо кучи .py
- ✅ Быстрее запуск (скомпилированный код)
- ✅ Проще распространять

## 📦 Установка Nuitka

### Windows
```bash
pip install nuitka

# Для Python 3.12+ требуется Cython
pip install cython
```

### Linux/macOS
```bash
pip3 install nuitka

# Для Python 3.12+ требуется Cython
pip3 install cython

# Дополнительно для Linux (для лучшей оптимизации)
sudo apt-get install ccache  # Ubuntu/Debian
sudo dnf install ccache      # Fedora
```

### Важно для Python 3.12+
Начиная с Python 3.12, Nuitka требует Cython для компиляции. Установите:
```bash
pip install cython>=3.0.0
```

Если Cython не установлен, Nuitka может выдать ошибку:
```
Error: Nuitka requires Cython for Python 3.12+ support
```

## 🚀 Быстрая компиляция

### Windows
```bash
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

Это скомпилирует:
- `dist/kcm_chat.exe` (или `kcm_chat` на Unix) - клиент
- `dist/kcm_chat_server.exe` (или `kcm_chat_server`) - сервер

## 🔧 Ручная компиляция

### Клиент
```bash
python -m nuitka \
    --standalone \
    --onefile \
    --output-filename=kcm_chat \
    --output-dir=dist \
    --lto=yes \
    --include-package=kcmpy \
    --include-package=socketio \
    chat_client_simple_notifications.py
```

### Сервер
```bash
python -m nuitka \
    --standalone \
    --onefile \
    --output-filename=kcm_chat_server \
    --output-dir=dist \
    --include-package=flask \
    --include-package=flask_socketio \
    chat_server.py
```

## 🎨 Интерактивная компиляция

```bash
python build_nuitka.py
```

Выберите что компилировать:
1. Только клиент
2. Только сервер
3. Оба
4. Выход

## ⚙️ Параметры Nuitka

### Основные
- `--standalone` - включить все зависимости
- `--onefile` - один исполняемый файл
- `--output-filename=NAME` - имя выходного файла
- `--output-dir=DIR` - директория для вывода

### Оптимизация
- `--lto=yes` - Link Time Optimization (быстрее, меньше размер)
- `--python-flag=no_site` - не включать site.py

### Включение/исключение модулей
- `--include-package=PKG` - включить пакет
- `--nofollow-import-to=PKG` - не следовать импортам в пакет

### Windows специфичные
- `--windows-console-mode=attach` - консольное приложение
- `--windows-icon-from-ico=icon.ico` - иконка приложения

## 📊 Размеры файлов

Примерные размеры после компиляции:

| Файл | Windows | Linux |
|------|---------|-------|
| Клиент | ~15-20 MB | ~12-18 MB |
| Сервер | ~18-25 MB | ~15-22 MB |

Размер зависит от:
- Включенных зависимостей
- Оптимизаций
- Платформы

## 🐛 Решение проблем

### Nuitka не найден
```bash
pip install --upgrade nuitka
```

### Ошибка компиляции
1. Проверьте что все зависимости установлены:
   ```bash
   pip install -r requirements.txt
   ```

2. Попробуйте без оптимизаций:
   ```bash
   python -m nuitka --standalone --onefile chat_client_simple_notifications.py
   ```

3. Проверьте логи в `dist/` директории

### Долгая компиляция
Первая компиляция может занять 5-15 минут.
Последующие будут быстрее благодаря кэшированию.

Ускорение:
```bash
# Linux
sudo apt-get install ccache

# Windows
# Nuitka автоматически использует кэш
```

### Большой размер файла
Исключите ненужные модули:
```bash
--nofollow-import-to=tkinter \
--nofollow-import-to=matplotlib \
--nofollow-import-to=numpy \
--nofollow-import-to=pandas
```

### Антивирус блокирует
Некоторые антивирусы могут блокировать скомпилированные файлы.
Добавьте в исключения или используйте `--windows-uac-admin` для подписи.

## 📝 Настройки сохраняются

После компиляции настройки сохраняются в:
- **Windows**: `C:\Users\<USER>\.kcm\kcm_chat.json`
- **Linux**: `~/.kcm/kcm_chat.json`
- **macOS**: `~/.kcm/kcm_chat.json`

Формат:
```json
{
  "server": {
    "url": "http://localhost:5000"
  },
  "user": {
    "nickname": "Пользователь"
  },
  "notifications": {
    "messages": true,
    "joins": true,
    "leaves": false
  }
}
```

## 🚀 Распространение

### Один файл
Просто скопируйте `kcm_chat.exe` (или `kcm_chat`) на целевую машину.

### С сервером
Скопируйте оба файла:
- `kcm_chat.exe` - клиент
- `kcm_chat_server.exe` - сервер

### Архив
```bash
# Windows
7z a kcm_chat.zip dist/kcm_chat.exe dist/kcm_chat_server.exe

# Linux
tar -czf kcm_chat.tar.gz dist/kcm_chat dist/kcm_chat_server
```

## 💡 Советы

1. **Тестируйте скомпилированную версию** перед распространением
2. **Используйте --lto=yes** для оптимизации
3. **Исключайте ненужные модули** для уменьшения размера
4. **Добавьте иконку** для Windows версии
5. **Создайте installer** для удобства (NSIS, Inno Setup)

## 📚 Дополнительно

### Создание installer (Windows)
Используйте Inno Setup:
```iss
[Setup]
AppName=KCM Chat
AppVersion=0.1.0
DefaultDirName={pf}\KCM Chat
OutputBaseFilename=kcm_chat_setup

[Files]
Source: "dist\kcm_chat.exe"; DestDir: "{app}"
Source: "dist\kcm_chat_server.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\KCM Chat"; Filename: "{app}\kcm_chat.exe"
Name: "{group}\KCM Chat Server"; Filename: "{app}\kcm_chat_server.exe"
```

### Создание .deb пакета (Linux)
```bash
mkdir -p kcm-chat/usr/local/bin
cp dist/kcm_chat kcm-chat/usr/local/bin/
cp dist/kcm_chat_server kcm-chat/usr/local/bin/

mkdir -p kcm-chat/DEBIAN
cat > kcm-chat/DEBIAN/control << EOF
Package: kcm-chat
Version: 0.1.0
Architecture: amd64
Maintainer: Your Name
Description: KCM Chat Client and Server
EOF

dpkg-deb --build kcm-chat
```

## 🔗 Ссылки

- [Nuitka Documentation](https://nuitka.net/doc/user-manual.html)
- [Nuitka GitHub](https://github.com/Nuitka/Nuitka)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Версия:** 0.1.0  
**Дата:** 2026-02-24

# KCM Chat - Compilation Guide

## 🎯 Why Compile?

Compiling with Nuitka creates standalone executable files:
- ✅ No Python required on the target machine
- ✅ Single file instead of multiple .py files
- ✅ Faster startup (compiled code)
- ✅ Easier distribution

## 📦 Installing Nuitka

### Windows
```bash
pip install nuitka

# Cython required for Python 3.12+
pip install cython
```

### Linux/macOS
```bash
pip3 install nuitka

# Cython required for Python 3.12+
pip3 install cython

# Additional for Linux (better optimization)
sudo apt-get install ccache  # Ubuntu/Debian
sudo dnf install ccache      # Fedora
```

### Important for Python 3.12+
Starting with Python 3.12, Nuitka requires Cython for compilation. Install it:
```bash
pip install cython>=3.0.0
```

If Cython is not installed, Nuitka may throw an error:
```
Error: Nuitka requires Cython for Python 3.12+ support
```

## 🚀 Quick Compilation

### Windows
```bash
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

This will compile:
- `dist/kcm_chat.exe` (or `kcm_chat` on Unix) - client
- `dist/kcm_chat_server.exe` (or `kcm_chat_server`) - server

## 🔧 Manual Compilation

### Client
```bash
python -m nuitka \
    --standalone \
    --onefile \
    --output-filename=kcm_chat \
    --output-dir=dist \
    --lto=yes \
    --include-package=kcmpy \
    --include-package=socketio \
    chat_client.py
```

### Server
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

## ⚙️ Interactive Compilation

```bash
python build_nuitka.py
```

Select what to compile:
1. Client only
2. Server only
3. Both
4. Exit

## ⚙️ Nuitka Options

### Main Options
- `--standalone` - include all dependencies
- `--onefile` - single executable file
- `--output-filename=NAME` - output file name
- `--output-dir=DIR` - output directory

### Optimization
- `--lto=yes` - Link Time Optimization (faster, smaller size)
- `--python-flag=no_site` - don't include site.py

### Include/Exclude Modules
- `--include-package=PKG` - include package
- `--nofollow-import-to=PKG` - don't follow imports to package

### Windows Specific
- `--windows-console-mode=attach` - console application
- `--windows-icon-from-ico=icon.ico` - application icon

## 📊 File Sizes

Approximate sizes after compilation:

| File | Windows | Linux |
|------|---------|-------|
| Client | ~15-20 MB | ~12-18 MB |
| Server | ~18-25 MB | ~15-22 MB |

Size depends on:
- Included dependencies
- Optimizations
- Platform

## 🐛 Troubleshooting

### Nuitka Not Found
```bash
pip install --upgrade nuitka
```

### Compilation Error
1. Check that all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Try without optimizations:
   ```bash
   python -m nuitka --standalone --onefile chat_client.py
   ```

3. Check logs in the `dist/` directory

### Long Compilation Time
First compilation may take 5-15 minutes.
Subsequent compilations will be faster thanks to caching.

Speed up:
```bash
# Linux
sudo apt-get install ccache

# Windows
# Nuitka automatically uses cache
```

### Large File Size
Exclude unnecessary modules:
```bash
--nofollow-import-to=tkinter \
--nofollow-import-to=matplotlib \
--nofollow-import-to=numpy \
--nofollow-import-to=pandas
```

### Antivirus Blocking
Some antivirus software may block compiled files.
Add to exceptions or use `--windows-uac-admin` for signing.

## 📝 Settings Persistence

After compilation, settings are saved to:
- **Windows**: `C:\Users\<USER>\.kcm\kcm_chat.json`
- **Linux**: `~/.kcm/kcm_chat.json`
- **macOS**: `~/.kcm/kcm_chat.json`

Format:
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

## 🚀 Distribution

### Single File
Simply copy `kcm_chat.exe` (or `kcm_chat`) to the target machine.

### With Server
Copy both files:
- `kcm_chat.exe` - client
- `kcm_chat_server.exe` - server

### Archive
```bash
# Windows
7z a kcm_chat.zip dist/kcm_chat.exe dist/kcm_chat_server.exe

# Linux
tar -czf kcm_chat.tar.gz dist/kcm_chat dist/kcm_chat_server
```

## 💡 Tips

1. **Test the compiled version** before distribution
2. **Use --lto=yes** for optimization
3. **Exclude unnecessary modules** to reduce size
4. **Add icon** for Windows version
5. **Create installer** for convenience (NSIS, Inno Setup)

## 📚 Additional

### Creating Installer (Windows)
Use Inno Setup:
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

### Creating .deb Package (Linux)
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

## 🔗 Links

- [Nuitka Documentation](https://nuitka.net/doc/user-manual.html)
- [Nuitka GitHub](https://github.com/Nuitka/Nuitka)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Version:** 0.1.0
**Date:** 2026-02-24

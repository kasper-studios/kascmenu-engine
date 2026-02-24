#!/bin/bash
# Quick build script for Linux/macOS

echo "========================================"
echo "  KCM Chat - Nuitka Build (Unix)"
echo "========================================"
echo

# Check Python version
python3 -c "import sys; v=sys.version_info; print(f'Python {v.major}.{v.minor}.{v.micro}')"
python3 -c "import sys; v=sys.version_info; exit(0 if v.major==3 and v.minor>=12 else 1)" &> /dev/null
NEEDS_CYTHON=$?

# Check if Nuitka is installed
if ! python3 -m nuitka --version &> /dev/null; then
    echo "[ERROR] Nuitka not installed!"
    echo "Install: pip install nuitka"
    if [ $NEEDS_CYTHON -eq 0 ]; then
        echo "For Python 3.12+ also install: pip install cython"
    fi
    exit 1
fi

# Check Cython if needed
if [ $NEEDS_CYTHON -eq 0 ]; then
    if ! python3 -c "import cython" &> /dev/null; then
        echo "[ERROR] Cython required for Python 3.12+!"
        echo "Install: pip install cython>=3.0.0"
        exit 1
    fi
fi

echo "[1/2] Building Client..."
python3 -m nuitka \
    --standalone \
    --onefile \
    --enable-plugin=no-qt \
    --assume-yes-for-downloads \
    --output-filename=kcm_chat \
    --output-dir=dist \
    --lto=yes \
    --python-flag=no_site \
    --include-package=kcmpy \
    --include-package=socketio \
    --nofollow-import-to=tkinter \
    --nofollow-import-to=matplotlib \
    chat_client_simple_notifications.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Client build failed!"
    exit 1
fi

echo
echo "[2/2] Building Server..."
python3 -m nuitka \
    --standalone \
    --onefile \
    --enable-plugin=no-qt \
    --assume-yes-for-downloads \
    --output-filename=kcm_chat_server \
    --output-dir=dist \
    --lto=yes \
    --python-flag=no_site \
    --include-package=flask \
    --include-package=flask_socketio \
    --nofollow-import-to=tkinter \
    chat_server.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Server build failed!"
    exit 1
fi

echo
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo
echo "Files created in dist/:"
echo "  - kcm_chat (Client)"
echo "  - kcm_chat_server (Server)"
echo
echo "Make executable:"
echo "  chmod +x dist/kcm_chat"
echo "  chmod +x dist/kcm_chat_server"
echo

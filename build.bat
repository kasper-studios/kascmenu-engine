@echo off
REM Quick build script for Windows

echo ========================================
echo   KCM Chat - Nuitka Build (Windows)
echo ========================================
echo.

REM Check Python version
python -c "import sys; v=sys.version_info; print(f'Python {v.major}.{v.minor}.{v.micro}')"
python -c "import sys; v=sys.version_info; exit(0 if v.major==3 and v.minor>=12 else 1)" >nul 2>&1
set NEEDS_CYTHON=%errorlevel%

REM Check if Nuitka is installed
python -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Nuitka not installed!
    echo Install: pip install nuitka
    if %NEEDS_CYTHON%==0 (
        echo For Python 3.12+ also install: pip install cython
    )
    pause
    exit /b 1
)

REM Check Cython if needed
if %NEEDS_CYTHON%==0 (
    python -c "import cython" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Cython required for Python 3.12+!
        echo Install: pip install cython>=3.0.0
        pause
        exit /b 1
    )
)

echo [1/2] Building Client...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --enable-plugin=no-qt ^
    --assume-yes-for-downloads ^
    --output-filename=kcm_chat.exe ^
    --output-dir=dist ^
    --lto=yes ^
    --python-flag=no_site ^
    --include-package=kcmpy ^
    --include-package=socketio ^
    --nofollow-import-to=tkinter ^
    --nofollow-import-to=matplotlib ^
    --windows-console-mode=attach ^
    chat_client_simple_notifications.py

if errorlevel 1 (
    echo [ERROR] Client build failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Building Server...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --enable-plugin=no-qt ^
    --assume-yes-for-downloads ^
    --output-filename=kcm_chat_server.exe ^
    --output-dir=dist ^
    --lto=yes ^
    --python-flag=no_site ^
    --include-package=flask ^
    --include-package=flask_socketio ^
    --nofollow-import-to=tkinter ^
    --windows-console-mode=attach ^
    chat_server.py

if errorlevel 1 (
    echo [ERROR] Server build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Files created in dist/:
echo   - kcm_chat.exe (Client)
echo   - kcm_chat_server.exe (Server)
echo.
pause

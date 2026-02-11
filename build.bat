@echo off
REM THENUX Fixed Build Script - OneDIR Mode (Most Reliable)
REM This creates a folder with the EXE instead of a single file

echo ============================================
echo THENUX Executable Builder (Fixed Version)
echo ============================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo OK
echo.

REM Install PyInstaller
echo [2/6] Installing/Updating PyInstaller...
pip install --upgrade pyinstaller
echo.

REM Install dependencies
echo [3/6] Installing dependencies...
pip install vosk sounddevice soundfile edge-tts pycaw comtypes pillow requests pyautogui google-search-results
echo.

REM Check for Vosk model
echo [4/6] Checking Vosk model...
if not exist "vosk-model-small-en-us-0.15" (
    echo.
    echo ============================================
    echo WARNING: Vosk model not found!
    echo ============================================
    echo.
    echo The build will continue, but you'll need to:
    echo 1. Download: vosk-model-small-en-us-0.15
    echo 2. Place it in the dist\THENUX\ folder after building
    echo.
    echo Download from: https://alphacephei.com/vosk/models
    echo.
    pause
) else (
    echo Vosk model found!
)
echo.

REM Clean old builds
echo [5/6] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
echo.

REM Build
echo [6/6] Building THENUX (OneDIR mode)...
echo This may take 3-5 minutes...
echo.

pyinstaller --name=THENUX ^
    --onedir ^
    --console ^
    --add-data "face.png;." ^
    --add-data "core/prompt.txt;core" ^
    --hidden-import=vosk ^
    --hidden-import=sounddevice ^
    --hidden-import=soundfile ^
    --hidden-import=edge_tts ^
    --hidden-import=serpapi ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=PIL.ImageDraw ^
    --hidden-import=PIL.ImageFilter ^
    --hidden-import=requests ^
    --hidden-import=pyautogui ^
    --hidden-import=pycaw ^
    --hidden-import=comtypes ^
    --collect-all=vosk ^
    main.py

echo.

if exist "dist\THENUX\THENUX.exe" (
    echo ============================================
    echo SUCCESS! Build complete!
    echo ============================================
    echo.
    echo Your EXE is located at: dist\THENUX\THENUX.exe
    echo.
    
    REM Copy Vosk model if it exists
    if exist "vosk-model-small-en-us-0.15" (
        echo Copying Vosk model to dist folder...
        xcopy /E /I /Y "vosk-model-small-en-us-0.15" "dist\THENUX\vosk-model-small-en-us-0.15"
        echo.
        echo ============================================
        echo READY TO USE!
        echo ============================================
        echo.
        echo You can now:
        echo 1. Run dist\THENUX\THENUX.exe
        echo 2. OR zip the entire dist\THENUX folder to share
        echo.
    ) else (
        echo.
        echo ============================================
        echo IMPORTANT: Manual step required!
        echo ============================================
        echo.
        echo You need to copy the Vosk model:
        echo 1. Download: vosk-model-small-en-us-0.15
        echo 2. Copy it to: dist\THENUX\
        echo.
        echo Then you can run: dist\THENUX\THENUX.exe
        echo.
    )
) else (
    echo ============================================
    echo BUILD FAILED!
    echo ============================================
    echo.
    echo Please check the errors above.
    echo.
)

pause
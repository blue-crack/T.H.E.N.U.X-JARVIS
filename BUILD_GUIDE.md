# Complete EXE Build Guide for THENUX

## Prerequisites

1. **Python 3.8+** installed from https://python.org/downloads/
2. **All dependencies** installed: `pip install -r REQUIREMENTS.txt`
3. **PyInstaller** installed: `pip install pyinstaller`
4. **Vosk model** downloaded and extracted

## Quick Build

### Windows:
```batch
build.bat
```

### Linux/Mac:
```bash
chmod +x build.sh
./build.sh
```

## Manual Build

### Using Spec File:
```bash
pyinstaller thenux.spec
```

### Using Command Line (Windows):
```batch
pyinstaller --name=THENUX --onefile --windowed ^
--add-data "face.png;." ^
--add-data "core/prompt.txt;core" ^
--add-data "vosk-model-small-en-us-0.15;vosk-model-small-en-us-0.15" ^
--hidden-import=sounddevice --hidden-import=vosk --hidden-import=edge_tts ^
main.py
```

### Using Command Line (Linux/Mac):
```bash
pyinstaller --name=THENUX --onefile --windowed \
--add-data "face.png:." \
--add-data "core/prompt.txt:core" \
--add-data "vosk-model-small-en-us-0.15:vosk-model-small-en-us-0.15" \
--hidden-import=sounddevice --hidden-import=vosk --hidden-import=edge_tts \
main.py
```

## Output Location

Your executable will be created at:
- **Windows**: `dist/THENUX.exe`
- **Linux/Mac**: `dist/THENUX`

## File Size

Expect 200-500 MB due to:
- Vosk model (~40 MB)
- Python runtime (~20 MB)
- Dependencies (~140+ MB)

## Testing

1. Navigate to `dist` folder
2. Run `THENUX.exe` (or `./THENUX` on Linux/Mac)
3. Enter API keys when prompted
4. Test all features

## Common Issues

### "Module not found"
**Solution**: Add to hiddenimports in `thenux.spec`

### "face.png not found"
**Solution**: Ensure face.png is in root directory and added in datas

### "Vosk model not loading"
**Solution**: Check MODEL_PATH in speech_to_text.py

### Antivirus blocks EXE
**Solution**: Add exception or build on target machine

## Optimization

### Reduce Size:
1. Use smaller Vosk model
2. Enable UPX compression (already in spec)
3. Exclude unnecessary packages

### Debug Build:
```bash
pyinstaller --debug=all thenux.spec
```

## Distribution

### Single File:
Share `dist/THENUX.exe` directly

### With Installer:
Use Inno Setup or NSIS to create installer

## Success Checklist

- [ ] EXE runs on clean machine
- [ ] All features work
- [ ] API key input works
- [ ] Voice recognition works
- [ ] TTS speaks responses
- [ ] All actions function (search, weather, open app, messages)

---

**Congratulations!** You've successfully built THENUX.exe!

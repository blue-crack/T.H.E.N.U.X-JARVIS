# THENUX - Advanced AI Assistant

**THENUX** (The Highly Efficient Neural User eXperience) is a voice-controlled AI assistant with a modern, animated interface.

## 🎉 What's New in This Version

### ✅ MICROPHONE ISSUE FIXED!
The AI no longer picks up its own voice! The microphone automatically stops listening when the AI speaks.

### 🚀 5 NEW ACTIONS ADDED:
1. **Calculator** - Natural language math calculations
2. **Timers** - Set multiple timers with voice alerts
3. **Notes** - Take and manage persistent notes
4. **System Control** - Control volume, lock, sleep, shutdown
5. **File Manager** - Manage files and folders

**Total: 10 powerful actions!**

## Quick Start

### 1. Download Vosk Model
- Visit: https://alphacephei.com/vosk/models
- Download: `vosk-model-small-en-us-0.15`
- Extract to the thenux_assistant folder

### 2. Install Dependencies
```bash
pip install -r REQUIREMENTS.txt
```

### 3. Get API Keys
- **OpenRouter**: https://openrouter.ai/settings/keys
- **SerpAPI**: https://serpapi.com/dashboard

### 4. Run THENUX
```bash
python main.py
```

## Features

### Core Features:
- 🎤 **Voice Recognition** (Vosk - offline)
- 🔊 **Text-to-Speech** (Edge TTS)
- 🧠 **AI Brain** (OpenRouter)
- 💾 **Memory System** (remembers preferences)

### 10 Powerful Actions:

1. **💬 Send Messages** - WhatsApp, Telegram
2. **📱 Open Apps** - Launch any application
3. **🌤️ Weather** - Real-time weather info
4. **🔍 Web Search** - Smart search results
5. **🧮 Calculator** - Natural language math
6. **⏰ Timers** - Multiple simultaneous timers
7. **📝 Notes** - Persistent note-taking
8. **🖥️ System Control** - Volume, lock, shutdown
9. **📁 File Manager** - Files and folders
10. **💬 Chat** - Natural conversation

## Voice Commands Examples

```
"Hey THENUX, open Chrome"
"Send a message to John on WhatsApp"
"What's the weather in London?"
"Search for Python tutorials"
"Calculate 25 times 4"
"Set a timer for 10 minutes"
"Take a note: Buy milk tomorrow"
"Show my notes"
"Lock the computer"
"Increase volume"
"Open Downloads folder"
"Mute" (stop speaking)
```

## Building EXE

```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

Your executable will be in `dist/THENUX.exe`

## Documentation

- **[FEATURES_GUIDE.md](FEATURES_GUIDE.md)** - Complete features guide with examples
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Building the EXE
- **[CHANGELOG_v2.0.md](CHANGELOG_v2.0.md)** - SHOW UPDATES

## License

MIT License - See LICENSE file

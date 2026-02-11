# THENUX Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Download Vosk Model (2 min)
1. Visit: https://alphacephei.com/vosk/models
2. Download: `vosk-model-small-en-us-0.15` (~40 MB)
3. Extract to the `thenux_assistant` folder
4. Update MODEL_PATH in `speech_to_text.py` if needed

### Step 2: Install Dependencies (2 min)
```bash
pip install -r REQUIREMENTS.txt
```

### Step 3: Get API Keys (1 min)
1. OpenRouter: https://openrouter.ai/settings/keys
2. SerpAPI: https://serpapi.com/dashboard

### Step 4: Run THENUX
```bash
python main.py
```

### Step 5: Configure
1. Enter your API keys in the setup window
2. Click "SAVE & CONTINUE"
3. Start talking!

## Voice Commands

- "Hey THENUX, open Chrome"
- "Send a message to John"
- "What's the weather in Tokyo?"
- "Search for Python tutorials"
- "Mute" or "Stop"

## Building EXE

### Windows:
```bash
build.bat
```

### Linux/Mac:
```bash
./build.sh
```

Your executable will be in the `dist` folder!

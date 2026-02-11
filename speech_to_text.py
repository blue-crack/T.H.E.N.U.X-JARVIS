import sounddevice as sd
import vosk
import queue
import sys
import json
import threading
from pathlib import Path
import os

def get_base_dir():
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()

# Try multiple possible locations for the Vosk model
MODEL_PATHS = [
    BASE_DIR / "vosk-model-small-en-us-0.15",
    Path("vosk-model-small-en-us-0.15"),
    Path.home() / "Downloads" / "THENUX-JARVIS" / "thenux_assistant" / "vosk-model-small-en-us-0.15",
]

MODEL_PATH = None
for path in MODEL_PATHS:
    if path.exists():
        MODEL_PATH = path
        print(f"✓ Found Vosk model at: {MODEL_PATH}")
        break

if MODEL_PATH is None:
    print("=" * 60)
    print("⚠️  VOSK MODEL NOT FOUND!")
    print("=" * 60)
    print("\nPlease download the Vosk model:")
    print("1. Visit: https://alphacephei.com/vosk/models")
    print("2. Download: vosk-model-small-en-us-0.15")
    print("3. Extract it to the same folder as THENUX.exe")
    print("\nThe folder should be named: vosk-model-small-en-us-0.15")
    print(f"\nExpected location: {BASE_DIR / 'vosk-model-small-en-us-0.15'}")
    print("=" * 60)
    input("\nPress Enter to exit...")
    sys.exit(1)

try:
    model = vosk.Model(str(MODEL_PATH))
    print("✓ Vosk model loaded successfully")
except Exception as e:
    print(f"✗ Error loading Vosk model: {e}")
    print(f"Model path: {MODEL_PATH}")
    input("\nPress Enter to exit...")
    sys.exit(1)

q = queue.Queue()
stop_listening_flag = threading.Event()
is_speaking = False  # Track if AI is currently speaking

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # Only record when AI is not speaking
    if not is_speaking:
        q.put(bytes(indata))

def clear_queue():
    """Clear the audio queue to prevent AI voice from being picked up"""
    while not q.empty():
        try:
            q.get_nowait()
        except queue.Empty:
            break

def set_speaking(speaking: bool):
    """Set whether AI is currently speaking"""
    global is_speaking
    is_speaking = speaking
    if speaking:
        clear_queue()  # Clear queue when AI starts speaking

def record_voice(prompt="🎙 I'm listening, sir..."):
    """
    Blocking call, returns the first recognized sentence.
    Only records when AI is not speaking.
    """
    # Clear any leftover audio before starting
    clear_queue()
    
    print(prompt)
    rec = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while not stop_listening_flag.is_set():
            try:
                data = q.get(timeout=0.1)
            except queue.Empty:
                continue
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text.strip():
                    print("👤 You:", text)
                    # Clear queue after getting text to avoid picking up echoes
                    clear_queue()
                    return text
    return ""
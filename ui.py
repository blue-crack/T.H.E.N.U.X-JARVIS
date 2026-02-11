import os
import json
import time
import random
import tkinter as tk
from tkinter import ttk
from collections import deque
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
from tkinter.scrolledtext import ScrolledText
import sys
from pathlib import Path

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()
CONFIG_DIR = BASE_DIR / "config"
API_FILE = CONFIG_DIR / "api_keys.json"

class ThenuxUI:
    def __init__(self, face_path, size=(1000, 800)):
        self.root = tk.Tk()
        self.root.title("T.H.E.N.U.X - The Highly Efficient Neural User eXperience")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Configure window
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')  # Maximize on Windows
        self.root.configure(bg="#000000")
        
        # Allow resizing
        self.root.resizable(True, True)
        
        # Bind keys for fullscreen toggle
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.end_fullscreen)
        
        self.is_fullscreen = False
        
        # Main container with gradient background
        self.main_frame = tk.Frame(self.root, bg="#000000")
        self.main_frame.pack(fill="both", expand=True)
        
        # ==================== TOP BAR ====================
        self.create_top_bar()
        
        # ==================== CENTER CONTENT ====================
        self.center_frame = tk.Frame(self.main_frame, bg="#000000")
        self.center_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Visualization
        self.left_panel = tk.Frame(self.center_frame, bg="#000000")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Animated orb canvas
        self.canvas = tk.Canvas(
            self.left_panel,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Status label under orb
        self.status_label = tk.Label(
            self.left_panel,
            text="🎤 Ready to listen...",
            font=("Segoe UI", 16, "bold"),
            fg="#00ff88",
            bg="#000000"
        )
        self.status_label.pack(pady=10)
        
        # Right panel - Chat/Logs
        self.right_panel = tk.Frame(self.center_frame, bg="#0a0a0a", relief="flat", bd=0)
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Chat header
        chat_header = tk.Frame(self.right_panel, bg="#0f0f0f", height=50)
        chat_header.pack(fill="x", pady=(0, 2))
        
        tk.Label(
            chat_header,
            text="💬 Conversation",
            font=("Segoe UI", 14, "bold"),
            fg="#00ff88",
            bg="#0f0f0f"
        ).pack(side="left", padx=15, pady=10)
        
        # Clear chat button
        self.clear_btn = tk.Button(
            chat_header,
            text="🗑️ Clear",
            command=self.clear_chat,
            font=("Segoe UI", 9),
            fg="#ffffff",
            bg="#1a1a1a",
            activebackground="#2a2a2a",
            activeforeground="#00ff88",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        self.clear_btn.pack(side="right", padx=15, pady=10)
        
        # Chat area with custom styling
        self.text_frame = tk.Frame(self.right_panel, bg="#0a0a0a")
        self.text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.text_box = ScrolledText(
            self.text_frame,
            fg="#e0e0e0",
            bg="#0f0f0f",
            insertbackground="#00ff88",
            selectbackground="#00ff88",
            selectforeground="#000000",
            borderwidth=0,
            wrap="word",
            font=("Consolas", 11),
            padx=15,
            pady=15,
            relief="flat"
        )
        self.text_box.pack(fill="both", expand=True)
        self.text_box.configure(state="disabled")
        
        # Configure text tags for styling
        self.text_box.tag_config("user", foreground="#00cfff", font=("Consolas", 11, "bold"))
        self.text_box.tag_config("ai", foreground="#00ff88", font=("Consolas", 11, "bold"))
        self.text_box.tag_config("system", foreground="#ffaa00", font=("Consolas", 10, "italic"))
        self.text_box.tag_config("error", foreground="#ff4444", font=("Consolas", 10, "bold"))
        self.text_box.tag_config("success", foreground="#44ff44", font=("Consolas", 10, "bold"))
        self.text_box.tag_config("timestamp", foreground="#666666", font=("Consolas", 9))
        
        # ==================== BOTTOM BAR ====================
        self.create_bottom_bar()
        
        # Animation variables
        self.size = (600, 600)
        self.face_base = None
        self.halo_base = None
        
        # Load face image
        try:
            self.face_base = (
                Image.open(face_path)
                .convert("RGBA")
                .resize(self.size, Image.LANCZOS)
            )
            self.halo_base = self._create_halo(self.size, radius=220, y_offset=-50)
        except Exception as e:
            print(f"Error loading face image: {e}")
            self.face_base = self._create_default_face()
            self.halo_base = self._create_halo(self.size, radius=220, y_offset=-50)
        
        self.speaking = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.halo_alpha = 70
        self.target_halo_alpha = 70
        self.last_target_time = time.time()
        
        self.typing_queue = deque()
        self.is_typing = False
        
        # Show setup if needed
        if not self._api_keys_exist():
            self._show_setup_ui()
        else:
            self.write_log("Welcome to THENUX! I'm ready to assist you.", "system")
        
        # Start animation
        self._animate()
        
        # Handle window resize
        self.canvas.bind('<Configure>', self._on_resize)
        
        # Close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def create_top_bar(self):
        """Create modern top bar with logo and controls"""
        top_bar = tk.Frame(self.main_frame, bg="#0a0a0a", height=70)
        top_bar.pack(fill="x", pady=(0, 5))
        top_bar.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(top_bar, bg="#0a0a0a")
        title_frame.pack(side="left", padx=20)
        
        tk.Label(
            title_frame,
            text="⚡ T.H.E.N.U.X",
            font=("Segoe UI", 24, "bold"),
            fg="#00ff88",
            bg="#0a0a0a"
        ).pack(side="left")
        
        tk.Label(
            title_frame,
            text="The Highly Efficient Neural User eXperience",
            font=("Segoe UI", 10),
            fg="#666666",
            bg="#0a0a0a"
        ).pack(side="left", padx=15)
        
        # Control buttons
        controls_frame = tk.Frame(top_bar, bg="#0a0a0a")
        controls_frame.pack(side="right", padx=20)
        
        # Fullscreen button
        self.fs_btn = tk.Button(
            controls_frame,
            text="🖵 Fullscreen",
            command=self.toggle_fullscreen,
            font=("Segoe UI", 9),
            fg="#ffffff",
            bg="#1a1a1a",
            activebackground="#2a2a2a",
            activeforeground="#00ff88",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        self.fs_btn.pack(side="left", padx=5)
        
        # Settings button
        settings_btn = tk.Button(
            controls_frame,
            text="⚙️ Settings",
            command=self._show_setup_ui,
            font=("Segoe UI", 9),
            fg="#ffffff",
            bg="#1a1a1a",
            activebackground="#2a2a2a",
            activeforeground="#00ff88",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        settings_btn.pack(side="left", padx=5)

    def create_bottom_bar(self):
        """Create bottom status bar"""
        bottom_bar = tk.Frame(self.main_frame, bg="#0a0a0a", height=40)
        bottom_bar.pack(fill="x", side="bottom")
        bottom_bar.pack_propagate(False)
        
        # Status indicators
        status_frame = tk.Frame(bottom_bar, bg="#0a0a0a")
        status_frame.pack(side="left", padx=20)
        
        self.status_indicators = {
            'mic': tk.Label(status_frame, text="🎤 Listening", font=("Segoe UI", 9), fg="#666666", bg="#0a0a0a"),
            'ai': tk.Label(status_frame, text="🤖 Idle", font=("Segoe UI", 9), fg="#666666", bg="#0a0a0a"),
            'net': tk.Label(status_frame, text="🌐 Connected", font=("Segoe UI", 9), fg="#00ff88", bg="#0a0a0a")
        }
        
        self.status_indicators['mic'].pack(side="left", padx=10)
        self.status_indicators['ai'].pack(side="left", padx=10)
        self.status_indicators['net'].pack(side="left", padx=10)
        
        # Version info
        tk.Label(
            bottom_bar,
            text="v2.0 Enhanced",
            font=("Segoe UI", 9),
            fg="#444444",
            bg="#0a0a0a"
        ).pack(side="right", padx=20)

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
        if self.is_fullscreen:
            self.fs_btn.config(text="🗗 Exit Fullscreen")
        else:
            self.fs_btn.config(text="🖵 Fullscreen")

    def end_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.fs_btn.config(text="🖵 Fullscreen")

    def _on_resize(self, event):
        """Handle window resize"""
        # Update canvas size
        pass

    def clear_chat(self):
        """Clear the chat display"""
        self.text_box.configure(state="normal")
        self.text_box.delete(1.0, tk.END)
        self.text_box.configure(state="disabled")
        self.write_log("Chat cleared.", "system")

    def _api_keys_exist(self):
        return os.path.exists(API_FILE)

    def _show_setup_ui(self):
        """Modern setup dialog"""
        # Create modal window
        setup_window = tk.Toplevel(self.root)
        setup_window.title("THENUX Setup")
        setup_window.geometry("600x400")
        setup_window.configure(bg="#0f0f0f")
        setup_window.resizable(False, False)
        
        # Center the window
        setup_window.transient(self.root)
        setup_window.grab_set()
        
        # Header
        header = tk.Frame(setup_window, bg="#1a1a1a", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⚙️ THENUX Setup",
            font=("Segoe UI", 20, "bold"),
            fg="#00ff88",
            bg="#1a1a1a"
        ).pack(pady=25)
        
        # Content
        content = tk.Frame(setup_window, bg="#0f0f0f")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # OpenRouter API Key
        tk.Label(
            content,
            text="OpenRouter API Key *",
            font=("Segoe UI", 11, "bold"),
            fg="#00ff88",
            bg="#0f0f0f",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        tk.Label(
            content,
            text="Get your free key at: https://openrouter.ai/settings/keys",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="#0f0f0f",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.openrouter_entry = tk.Entry(
            content,
            font=("Consolas", 10),
            fg="#ffffff",
            bg="#1a1a1a",
            insertbackground="#00ff88",
            relief="flat",
            bd=0
        )
        self.openrouter_entry.pack(fill="x", ipady=10, pady=(0, 20))
        
        # SerpAPI Key
        tk.Label(
            content,
            text="SerpAPI Key (Optional)",
            font=("Segoe UI", 11, "bold"),
            fg="#00ff88",
            bg="#0f0f0f",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        tk.Label(
            content,
            text="Get 100 free searches at: https://serpapi.com/dashboard",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="#0f0f0f",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.serpapi_entry = tk.Entry(
            content,
            font=("Consolas", 10),
            fg="#ffffff",
            bg="#1a1a1a",
            insertbackground="#00ff88",
            relief="flat",
            bd=0
        )
        self.serpapi_entry.pack(fill="x", ipady=10, pady=(0, 30))
        
        # Save button
        def save_and_close():
            openrouter_key = self.openrouter_entry.get().strip()
            serpapi_key = self.serpapi_entry.get().strip()
            
            if not openrouter_key:
                tk.messagebox.showwarning("Missing Key", "OpenRouter API key is required!")
                return
            
            os.makedirs(CONFIG_DIR, exist_ok=True)
            
            with open(API_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "openrouter_api_key": openrouter_key,
                        "serpapi_api_key": serpapi_key
                    },
                    f,
                    indent=4
                )
            
            self.write_log("✓ API keys saved successfully!", "success")
            setup_window.destroy()
        
        save_btn = tk.Button(
            content,
            text="💾 Save & Continue",
            command=save_and_close,
            font=("Segoe UI", 12, "bold"),
            fg="#000000",
            bg="#00ff88",
            activebackground="#00dd77",
            activeforeground="#000000",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12
        )
        save_btn.pack(fill="x")

    def _create_halo(self, size, radius, y_offset):
        """Create animated halo effect"""
        w, h = size
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        cx = w // 2
        cy = h // 2 + y_offset

        for r in range(radius, 0, -12):
            alpha = int(70 * (1 - r / radius))
            draw.ellipse(
                (cx - r, cy - r, cx + r, cy + r),
                fill=(0, 255, 136, alpha)
            )

        return img.filter(ImageFilter.GaussianBlur(30))

    def _create_default_face(self):
        """Create default face if image not found"""
        img = Image.new("RGBA", self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw simple circle
        cx, cy = self.size[0] // 2, self.size[1] // 2
        r = min(cx, cy) - 50
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(0, 255, 136, 100))
        
        return img

    def write_log(self, text: str, tag="normal"):
        """Write to log with styling and timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.text_box.configure(state="normal")
        
        # Add timestamp
        self.text_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Determine prefix and tag based on message type
        if "You:" in text or text.startswith("You:"):
            prefix = "👤 "
            actual_tag = "user"
            text = text.replace("You:", "").strip()
        elif "AI:" in text or text.startswith("AI:") or "THENUX:" in text:
            prefix = "🤖 "
            actual_tag = "ai"
            text = text.replace("AI:", "").replace("THENUX:", "").strip()
        else:
            prefix = ""
            actual_tag = tag
        
        self.text_box.insert(tk.END, prefix + text + "\n\n", actual_tag)
        self.text_box.see(tk.END)
        self.text_box.configure(state="disabled")

    def start_speaking(self):
        """Called when AI starts speaking"""
        self.speaking = True
        self.status_label.config(text="🔊 Speaking...", fg="#ffaa00")
        self.status_indicators['ai'].config(text="🤖 Speaking", fg="#ffaa00")

    def stop_speaking(self):
        """Called when AI stops speaking"""
        self.speaking = False
        self.status_label.config(text="🎤 Listening...", fg="#00ff88")
        self.status_indicators['ai'].config(text="🤖 Idle", fg="#666666")

    def _animate(self):
        """Animate the orb"""
        now = time.time()

        if now - self.last_target_time > (0.25 if self.speaking else 0.7):
            if self.speaking:
                self.target_scale = random.uniform(1.05, 1.15)
                self.target_halo_alpha = random.randint(130, 180)
            else:
                self.target_scale = random.uniform(1.002, 1.008)
                self.target_halo_alpha = random.randint(50, 80)

            self.last_target_time = now

        scale_speed = 0.45 if self.speaking else 0.25
        halo_speed = 0.40 if self.speaking else 0.25

        self.scale += (self.target_scale - self.scale) * scale_speed
        self.halo_alpha += (self.target_halo_alpha - self.halo_alpha) * halo_speed

        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            # Create frame
            frame = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 255))

            # Scale and position halo
            halo = self.halo_base.copy()
            halo.putalpha(int(self.halo_alpha))
            halo_resized = halo.resize((canvas_width, canvas_height), Image.LANCZOS)
            frame.alpha_composite(halo_resized)

            # Scale and position face
            face_size = min(canvas_width, canvas_height) - 100
            face = self.face_base.resize(
                (int(face_size * self.scale), int(face_size * self.scale)),
                Image.LANCZOS
            )

            fx = (canvas_width - face.size[0]) // 2
            fy = (canvas_height - face.size[1]) // 2
            
            # Create temp image for composite
            temp = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
            temp.paste(face, (fx, fy), face)
            frame.alpha_composite(temp)

            # Convert to PhotoImage
            img = ImageTk.PhotoImage(frame)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=img)
            self.canvas.image = img

        self.root.after(16, self._animate)

    def _on_closing(self):
        """Handle window close"""
        if tk.messagebox.askokcancel("Quit", "Do you want to quit THENUX?"):
            os._exit(0)
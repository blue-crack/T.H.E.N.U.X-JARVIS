"""
System control action - Control computer functions
"""
import os
import platform
import subprocess
from tts import edge_speak


def system_control(parameters: dict, player=None, session_memory=None):
    """
    Control system functions.
    
    Parameters:
        - action (str): shutdown, restart, sleep, lock, volume_up, volume_down, mute
        - confirm (bool): Whether confirmed (for destructive actions)
        
    Examples:
        - "Lock the computer"
        - "Increase volume"
        - "Mute the sound"
        - "Put computer to sleep"
    """
    
    action = parameters.get("action", "").lower()
    confirm = parameters.get("confirm", False)
    
    if not action:
        msg = "Sir, what would you like me to do?"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    os_type = platform.system()
    
    try:
        # Volume controls
        if action in ["volume_up", "increase_volume", "louder"]:
            if os_type == "Windows":
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
            
            msg = "Volume increased, sir."
            
        elif action in ["volume_down", "decrease_volume", "quieter"]:
            if os_type == "Windows":
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
            
            msg = "Volume decreased, sir."
            
        elif action in ["mute", "silence", "unmute"]:
            if os_type == "Windows":
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                is_muted = volume.GetMute()
                volume.SetMute(not is_muted, None)
                
                msg = "Unmuted, sir." if is_muted else "Muted, sir."
            else:
                msg = "Mute control not available on this system, sir."
        
        # Lock screen
        elif action in ["lock", "lock_screen", "lock_computer"]:
            if os_type == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            elif os_type == "Darwin":  # macOS
                subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
            else:  # Linux
                subprocess.run(["xdg-screensaver", "lock"])
            
            msg = "Locking the screen, sir."
        
        # Sleep
        elif action in ["sleep", "suspend", "hibernate"]:
            if not confirm:
                msg = "Sir, are you sure you want to put the computer to sleep? Say 'confirm sleep' to proceed."
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            if os_type == "Windows":
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
            elif os_type == "Darwin":
                subprocess.run(["pmset", "sleepnow"])
            else:
                subprocess.run(["systemctl", "suspend"])
            
            msg = "Putting the computer to sleep, sir."
        
        # Shutdown
        elif action in ["shutdown", "shut_down", "power_off"]:
            if not confirm:
                msg = "Sir, are you sure you want to shutdown? Say 'confirm shutdown' to proceed."
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            if os_type == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "5"])
            elif os_type == "Darwin":
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            else:
                subprocess.run(["shutdown", "-h", "now"])
            
            msg = "Shutting down in 5 seconds, sir."
        
        # Restart
        elif action in ["restart", "reboot"]:
            if not confirm:
                msg = "Sir, are you sure you want to restart? Say 'confirm restart' to proceed."
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            if os_type == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "5"])
            elif os_type == "Darwin":
                subprocess.run(["sudo", "shutdown", "-r", "now"])
            else:
                subprocess.run(["reboot"])
            
            msg = "Restarting in 5 seconds, sir."
        
        else:
            msg = f"Sir, I don't recognize the action '{action}'."
        
        if player:
            player.write_log(f"THENUX: {msg}")
        
        edge_speak(msg, player)
        return msg
        
    except Exception as e:
        msg = f"Sir, I couldn't perform that action. {str(e)}"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg

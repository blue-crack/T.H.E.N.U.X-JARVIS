"""
File manager action - Create, read, and manage files
"""
import os
import subprocess
from pathlib import Path
from tts import edge_speak
import sys


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def file_manager(parameters: dict, player=None, session_memory=None):
    """
    Manage files and folders.
    
    Parameters:
        - action (str): open_folder, create_file, create_folder, delete, rename
        - path (str): File/folder path
        - new_name (str): New name for rename
        - content (str): Content for new files
        
    Examples:
        - "Open Downloads folder"
        - "Create a file called todo.txt"
        - "Create folder called Projects"
        - "Open My Documents"
    """
    
    action = parameters.get("action", "").lower()
    path = parameters.get("path", "").strip()
    
    if not action:
        msg = "Sir, what would you like me to do with files?"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    try:
        # Open folder
        if action in ["open_folder", "open_directory", "show_folder"]:
            # Common folder shortcuts
            shortcuts = {
                "downloads": str(Path.home() / "Downloads"),
                "documents": str(Path.home() / "Documents"),
                "desktop": str(Path.home() / "Desktop"),
                "pictures": str(Path.home() / "Pictures"),
                "music": str(Path.home() / "Music"),
                "videos": str(Path.home() / "Videos"),
            }
            
            path_lower = path.lower()
            if path_lower in shortcuts:
                path = shortcuts[path_lower]
            elif not path:
                path = str(Path.home())
            
            # Open folder
            if os.path.exists(path):
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", path])
                else:
                    subprocess.run(["xdg-open", path])
                
                msg = f"Opening {path}, sir."
            else:
                msg = f"Sir, the folder '{path}' doesn't exist."
        
        # Create file
        elif action in ["create_file", "new_file", "make_file"]:
            if not path:
                msg = "Sir, what should I name the file?"
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            # Add .txt if no extension
            if '.' not in path:
                path = f"{path}.txt"
            
            # Create in Documents if no path specified
            if os.path.sep not in path and '/' not in path:
                path = str(Path.home() / "Documents" / path)
            
            content = parameters.get("content", "")
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            msg = f"Created file {Path(path).name}, sir."
            
            # Open the file
            if sys.platform == "win32":
                os.startfile(path)
            
        # Create folder
        elif action in ["create_folder", "new_folder", "make_folder", "make_directory"]:
            if not path:
                msg = "Sir, what should I name the folder?"
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            # Create in Documents if no path specified
            if os.path.sep not in path and '/' not in path:
                path = str(Path.home() / "Documents" / path)
            
            os.makedirs(path, exist_ok=True)
            msg = f"Created folder {Path(path).name}, sir."
        
        # Delete file/folder
        elif action in ["delete", "remove", "delete_file"]:
            if not path:
                msg = "Sir, which file should I delete?"
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
            
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    msg = f"Deleted file {Path(path).name}, sir."
                else:
                    import shutil
                    shutil.rmtree(path)
                    msg = f"Deleted folder {Path(path).name}, sir."
            else:
                msg = f"Sir, '{path}' doesn't exist."
        
        else:
            msg = f"Sir, I don't recognize the action '{action}'."
        
        if player:
            player.write_log(f"THENUX: {msg}")
        
        edge_speak(msg, player)
        return msg
        
    except Exception as e:
        msg = f"Sir, I couldn't complete that file operation. {str(e)}"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg

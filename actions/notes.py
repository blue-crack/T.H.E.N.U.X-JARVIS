"""
Note-taking action - Take and manage notes
"""
import os
import json
from datetime import datetime
from pathlib import Path
from tts import edge_speak
import sys


def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
NOTES_DIR = BASE_DIR / "notes"
NOTES_FILE = NOTES_DIR / "notes.json"


def ensure_notes_dir():
    """Create notes directory if it doesn't exist"""
    NOTES_DIR.mkdir(exist_ok=True)


def load_notes():
    """Load notes from file"""
    if not NOTES_FILE.exists():
        return []
    
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_notes(notes):
    """Save notes to file"""
    ensure_notes_dir()
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def take_note(parameters: dict, player=None, session_memory=None):
    """
    Take a note.
    
    Parameters:
        - content (str): The note content
        - title (str): Optional title for the note
        
    Examples:
        - "Take a note: Buy milk tomorrow"
        - "Remember to call John at 3 PM"
        - "Note: Meeting with Sarah on Friday"
    """
    
    content = parameters.get("content", "").strip()
    title = parameters.get("title", "").strip()
    
    if not content:
        msg = "Sir, what would you like me to note?"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    # Load existing notes
    notes = load_notes()
    
    # Create new note
    note = {
        'id': len(notes) + 1,
        'title': title if title else f"Note {len(notes) + 1}",
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    notes.append(note)
    save_notes(notes)
    
    msg = f"Noted, sir. {title if title else 'Note saved'}."
    
    if player:
        player.write_log(f"THENUX: 📝 {msg}")
        player.write_log(f"Content: {content}")
    
    edge_speak(msg, player)
    
    return msg


def list_notes(parameters: dict, player=None, session_memory=None):
    """
    List all notes or search notes.
    
    Parameters:
        - search (str): Optional search term
        - limit (int): Number of notes to show (default: 5)
    """
    
    notes = load_notes()
    search_term = parameters.get("search", "").lower()
    limit = parameters.get("limit", 5)
    
    if not notes:
        msg = "You have no notes, sir."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    # Filter by search term if provided
    if search_term:
        notes = [n for n in notes if search_term in n['content'].lower() or search_term in n['title'].lower()]
        
        if not notes:
            msg = f"No notes found matching '{search_term}', sir."
            if player:
                player.write_log(f"THENUX: {msg}")
            edge_speak(msg, player)
            return msg
    
    # Get most recent notes
    recent_notes = sorted(notes, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    if player:
        player.write_log(f"\n📝 Your Notes ({len(notes)} total):")
        for note in recent_notes:
            player.write_log(f"\n[{note['date']}] {note['title']}")
            player.write_log(f"   {note['content']}")
    
    # Speak summary
    if len(recent_notes) == 1:
        msg = f"You have one note: {recent_notes[0]['title']}. {recent_notes[0]['content']}"
    else:
        titles = [n['title'] for n in recent_notes[:3]]
        msg = f"You have {len(notes)} notes, sir. Most recent: {', '.join(titles)}."
    
    edge_speak(msg, player)
    
    return msg


def delete_note(parameters: dict, player=None, session_memory=None):
    """
    Delete a note by ID or delete all notes.
    
    Parameters:
        - note_id (int): ID of note to delete
        - all (bool): Delete all notes
    """
    
    notes = load_notes()
    
    if not notes:
        msg = "You have no notes to delete, sir."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    delete_all = parameters.get("all", False)
    
    if delete_all:
        count = len(notes)
        save_notes([])
        msg = f"Deleted all {count} notes, sir."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    note_id = parameters.get("note_id")
    
    if not note_id:
        msg = "Sir, which note should I delete?"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    try:
        note_id = int(note_id)
        note = next((n for n in notes if n['id'] == note_id), None)
        
        if note:
            notes.remove(note)
            save_notes(notes)
            msg = f"Deleted note: {note['title']}, sir."
        else:
            msg = f"Note {note_id} not found, sir."
        
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        
        return msg
        
    except ValueError:
        msg = "Sir, I need a valid note ID."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg

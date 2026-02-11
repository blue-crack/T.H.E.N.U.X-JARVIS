"""
Timer and Alarm action - Set timers and alarms
"""
import time
import threading
from datetime import datetime, timedelta
from tts import edge_speak


active_timers = []


def set_timer(parameters: dict, player=None, session_memory=None):
    """
    Sets a timer or alarm.
    
    Parameters:
        - duration (int): Duration in seconds
        - unit (str): 'seconds', 'minutes', 'hours'
        - message (str): Optional message when timer ends
        
    Examples:
        - "Set a timer for 5 minutes"
        - "Remind me in 30 seconds"
        - "Set alarm for 2 hours"
    """
    
    duration = parameters.get("duration")
    unit = parameters.get("unit", "minutes").lower()
    message = parameters.get("message", "Timer complete")
    
    if not duration:
        msg = "Sir, how long should I set the timer for?"
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    try:
        duration = int(duration)
        
        # Convert to seconds
        if unit in ['second', 'seconds', 'sec', 'secs']:
            total_seconds = duration
        elif unit in ['minute', 'minutes', 'min', 'mins']:
            total_seconds = duration * 60
        elif unit in ['hour', 'hours', 'hr', 'hrs']:
            total_seconds = duration * 3600
        else:
            total_seconds = duration * 60  # Default to minutes
        
        # Create timer
        timer_id = len(active_timers)
        timer_info = {
            'id': timer_id,
            'duration': total_seconds,
            'message': message,
            'start_time': time.time()
        }
        active_timers.append(timer_info)
        
        # Confirm
        time_str = f"{duration} {unit}"
        confirm_msg = f"Timer set for {time_str}, sir."
        
        if player:
            player.write_log(f"THENUX: {confirm_msg}")
        edge_speak(confirm_msg, player)
        
        # Start timer thread
        def timer_thread():
            time.sleep(total_seconds)
            
            # Alert
            alert_msg = f"Sir, {message}. Time's up!"
            if player:
                player.write_log(f"⏰ THENUX: {alert_msg}")
            edge_speak(alert_msg, player)
            
            # Remove from active timers
            if timer_info in active_timers:
                active_timers.remove(timer_info)
        
        threading.Thread(target=timer_thread, daemon=True).start()
        
        return confirm_msg
        
    except ValueError:
        msg = "Sir, I need a valid number for the duration."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg


def check_timers(parameters: dict, player=None, session_memory=None):
    """
    Check active timers.
    """
    
    if not active_timers:
        msg = "No active timers, sir."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    current_time = time.time()
    timer_list = []
    
    for timer in active_timers:
        elapsed = current_time - timer['start_time']
        remaining = timer['duration'] - elapsed
        
        if remaining > 60:
            time_str = f"{int(remaining / 60)} minutes"
        else:
            time_str = f"{int(remaining)} seconds"
        
        timer_list.append(f"{timer['message']} in {time_str}")
    
    msg = f"Active timers: {', '.join(timer_list)}, sir."
    
    if player:
        player.write_log(f"THENUX: {msg}")
    edge_speak(msg, player)
    
    return msg


def cancel_timers(parameters: dict, player=None, session_memory=None):
    """
    Cancel all timers.
    """
    
    count = len(active_timers)
    active_timers.clear()
    
    msg = f"Cancelled {count} timer{'s' if count != 1 else ''}, sir."
    
    if player:
        player.write_log(f"THENUX: {msg}")
    edge_speak(msg, player)
    
    return msg

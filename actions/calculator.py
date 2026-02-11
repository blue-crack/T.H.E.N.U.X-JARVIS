"""
Calculator action - Perform mathematical calculations
"""
import re
from tts import edge_speak


def calculate(parameters: dict, player=None, session_memory=None):
    """
    Performs mathematical calculations.
    
    Parameters:
        - expression (str): Math expression to calculate
        
    Examples:
        - "What's 25 times 4?"
        - "Calculate 100 divided by 5"
        - "What's the square root of 144?"
    """
    
    expression = parameters.get("expression", "").strip()
    
    if not expression:
        msg = "Sir, I need a mathematical expression to calculate."
        if player:
            player.write_log(f"THENUX: {msg}")
        edge_speak(msg, player)
        return msg
    
    try:
        # Clean the expression
        expression = expression.lower()
        
        # Replace common words with operators
        replacements = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'multiplied by': '*',
            'divided by': '/',
            'over': '/',
            'percent': '/100*',
            'squared': '**2',
            'cubed': '**3',
        }
        
        for word, operator in replacements.items():
            expression = expression.replace(word, operator)
        
        # Handle special functions
        if 'square root' in expression or 'sqrt' in expression:
            import math
            number = re.search(r'\d+\.?\d*', expression)
            if number:
                result = math.sqrt(float(number.group()))
                msg = f"The square root is {result:.2f}, sir."
                if player:
                    player.write_log(f"THENUX: {msg}")
                edge_speak(msg, player)
                return msg
        
        # Remove non-mathematical characters
        expression = re.sub(r'[^0-9+\-*/.()^]', '', expression)
        
        # Handle exponents
        expression = expression.replace('^', '**')
        
        # Calculate
        result = eval(expression)
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 2)
        
        msg = f"The answer is {result}, sir."
        
        if player:
            player.write_log(f"THENUX: {expression} = {result}")
        
        edge_speak(msg, player)
        
        if session_memory:
            session_memory.set_last_calculation = result
        
        return msg
        
    except Exception as e:
        msg = f"Sir, I couldn't calculate that. Please rephrase the expression."
        if player:
            player.write_log(f"THENUX: {msg} (Error: {e})")
        edge_speak(msg, player)
        return msg

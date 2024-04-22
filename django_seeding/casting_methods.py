

def cast_to_bool(text: str):
    if isinstance(text, str):
        if text.lower() in ['true', '1', 't', 'y', 'yes']:
            return True
        elif text.lower() in ['false', '0', 'f', 'n', 'no']:
            return False
    return None

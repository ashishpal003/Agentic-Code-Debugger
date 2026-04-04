import re

def extract_missing_module(error: str):
    """
    Extract module name from error
    """
    match = re.search(r"No module named '(.+?)'", error)
    if match:
        return match.group(1)
    
    return None
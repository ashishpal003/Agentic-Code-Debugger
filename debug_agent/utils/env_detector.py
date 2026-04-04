import os

def detect_dependency_file(project_path):
    """
    Detect common dependency files
    """
    if os.path.exists(os.path.join(project_path, "requirements.txt")):
        return "requirements.txt"
    
    if os.path.exists(os.path.join(project_path, "pyproject.toml")):
        return "pyproject.toml"
    
    return None
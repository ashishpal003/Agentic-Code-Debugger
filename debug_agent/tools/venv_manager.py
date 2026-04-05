import subprocess
import os

def create_virtualenv(sandbox_path: str) -> str:
    """
    Create a virtual environment inside sandbox.

    Args:
        sandbox_path (str): Root sandbox directory

    Returns:
        str: Path to created virtual environment
    """
    
    venv_path = os.path.join(sandbox_path, "venv")

    subprocess.run(
        ["python", "-m", "venv", venv_path],
        capture_output=True
    )

    return venv_path
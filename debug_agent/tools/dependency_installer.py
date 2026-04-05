import subprocess
import os
from typing import Dict

def install_requirements(venv_path: str, sandbox_path: str) -> Dict:
    """
    Install dependencies from requirements.txt inside sandbox.

    Args:
        venv_path (str): Virtual environment path
        sandbox_path (str): Project root inside sandbox

    Returns:
        Dict: Installation result
    """

    req_file = os.path.join(sandbox_path, "requirements.txt")

    if not os.path.exists(req_file):
        return {
            "success": False,
            "message": "No requirements.txt found"
        }
    
    pip_exec = os.path.join(venv_path, "bin", "pip")
    
    result = subprocess.run(
        [pip_exec, "install", "-r", req_file],
        capture_output=True,
        text=True,
        timeout=60
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }
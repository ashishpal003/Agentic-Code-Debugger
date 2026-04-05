import subprocess
import os
from typing import Dict, Optional

def run_code(entry_point: str, cwd: str, venv_path: Optional[str] = None) -> Dict:
    """
    Execute a Python script inside a sandboxed environment.

    Args:
        entry_point (str): The main Python file to execute.
        cwd (str): Working directory (sandbox path).
        venv_path (Optional[str]): Path to virtual environment.

    Returns:
        Dict: Execution result containing:
            - success (bool)
            - stdout (str)
            - stderr (str)
            - exit_code (int)
    """

    try:
        # Use virtualenv Python if available
        python_exec = "python"
        if venv_path:
            python_exec = os.path.join(venv_path, "bin", "python")

        result = subprocess.run(
            [python_exec, entry_point],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=8 # Prevent infinite execution
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "",
            "error": "Execution timed out (possible infinite loop)",
            "exit_code": -1
        }
    
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": "",
            "error": str(e),
            "exit_code": -1
        }
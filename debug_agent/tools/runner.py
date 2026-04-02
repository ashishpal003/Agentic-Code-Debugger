import subprocess
from typing import Dict

def run_code(entry_point: str, cwd: str) -> Dict:
    """
    Run Python code safely inside sandbox
    """

    try:
        result = subprocess.run(
            ["python", entry_point],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5 # prevents infinite loops
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timed out",
            "exit_code": -1
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "exit_code": -1
        }
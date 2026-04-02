import subprocess
from typing import Dict

def lint_code(file_path: str) -> Dict:
    """
    Run Ruff linter on file
    """

    try:
        result = subprocess.run(
            ["ruff", "check", file_path],
            capture_output=True,
            text=True
        )

        return {
            "issue_found": result.returncode != 0,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        return {
            "issue_found": False,
            "error": str(e)
        }
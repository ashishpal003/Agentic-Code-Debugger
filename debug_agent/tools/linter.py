import subprocess
from typing import Dict

def lint_code(file_path: str) -> Dict:
    """
    Run Ruff linter on a Python file.

    Args:
        file_path (str): Path to Python file

    Returns:
        Dict: Lint result
    """

    try:
        result = subprocess.run(
            ["ruff", "check", file_path],
            capture_output=True,
            text=True
        )

        return {
            "issue_found": result.returncode != 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    
    except Exception as e:
        return {
            "issue_found": False,
            "error": str(e)
        }
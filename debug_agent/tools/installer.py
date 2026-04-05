import subprocess
import os
from typing import Dict

# Handle mismatched import vs pip package names
PACKAGE_MAPPING = {
    "sklearn": "scikit-learn"
}

def install_package(package: str, venv_path: str) -> Dict:
    """
    Install a Python package inside the sandbox virtual environment.

    Args:
        package (str): Package name to install.
        venv_path (str): Path to virtual environment.

    Returns:
        Dict: Installation result
    """
    try:
        pip_exec = os.path.join(venv_path, "bin", "pip")

        result = subprocess.run(
            [pip_exec, "install", package],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "package": package,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    
    except Exception as e:
        return {
            "success": False,
            "package": package,
            "error": str(e)
        }
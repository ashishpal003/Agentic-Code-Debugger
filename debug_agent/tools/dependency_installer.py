import subprocess
import os

def install_requirements(venv_path, sandbox_path):

    pip_path = os.path.join(venv_path, "bin", "pip")

    req_file = os.path.join(sandbox_path, "requirements.txt")

    if not os.path.exists(req_file):
        return {"success": False, "message": "No requirements.txt"}
    
    result = subprocess.run(
        [pip_path, "install", "-r", req_file],
        capture_output=True,
        text=True,
        timeout=60
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
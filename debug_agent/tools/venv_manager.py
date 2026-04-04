import subprocess
import os

def create_virtualenv(sandbox_path):
    venv_path = os.path.join(sandbox_path, "venv")

    subprocess.run(
        ["python", "-m", "venv", venv_path],
        capture_output=True
    )

    return venv_path
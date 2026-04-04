import subprocess

PACKAGE_MAPPING = {
    "sklearn": "scikit-learn"
}

def install_package(package: str, cwd: str):
    try:
        result = subprocess.run(
            ["pip", "install", package],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=20
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
import os
from pathlib import Path

project_name = "debug_agent"

file_folder = [
    f"{project_name}/__init__.py",
    f"{project_name}/agent/__init__.py",
    f"{project_name}/core/__init__.py",
    f"{project_name}/tools/__init__.py",
    f"{project_name}/sandbox/__init__.py",
    f"{project_name}/validation/__init__.py",
    f"{project_name}/observability/__init__.py",
    f"{project_name}/prompts/__init__.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"main.py",
    f"requirements.txt"
]

for file_path in file_folder:
    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.touch(exist_ok=True)
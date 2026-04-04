import os
import shutil
import tempfile

from debug_agent.tools.venv_manager import create_virtualenv
from debug_agent.tools.dependency_installer import install_requirements
from debug_agent.utils.env_detector import detect_dependency_file

class SandboxManager:

    def __init__(self, project_path, keep_sandbox=False):
        self.project_path = project_path
        self.sandbox_path = None
        self.keep_sandbox = False

    def setup(self):
        """
        Create isolated sandbox and copy projec/files
        """
        self.sandbox_path = tempfile.mkdtemp(prefix="debug-agent_")

        if os.path.isdir(self.project_path):
            # Full project
            shutil.copytree(
                self.project_path,
                self.sandbox_path,
                dirs_exist_ok=True
            )
        else:
            # Single file
            shutil.copy(self.project_path, self.sandbox_path)

        # 1. create venv
        venv_path = create_virtualenv(self.sandbox_path)

        # 2. detect dependency file
        dep_file = detect_dependency_file(self.sandbox_path)

        # 3. Install dependencies
        if dep_file == "requirements.txt":
            install_requirements(venv_path, self.sandbox_path)

        self.venv_path = venv_path

        return self.sandbox_path
    
    def get_path(self):
        return self.sandbox_path
    
    def cleanup(self):
        if self.keep_sandbox:
            print(f"[DEBUG] Sandbox retained at: {self.sandbox_path}")
            return
        
        if self.sandbox_path and os.path.exists(self.sandbox_path):
            shutil.rmtree(self.sandbox_path)
        
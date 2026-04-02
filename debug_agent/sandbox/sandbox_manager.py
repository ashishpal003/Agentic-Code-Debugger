import os
import shutil
import tempfile

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

        return self.sandbox_path
    
    def get_path(self):
        return self.sandbox_path
    
    def cleanup(self):
        if self.keep_sandbox:
            print(f"[DEBUG] Sandbox retained at: {self.sandbox_path}")
            return
        
        if self.sandbox_path and os.path.exists(self.sandbox_path):
            shutil.rmtree(self.sandbox_path)
        
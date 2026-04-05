import os
import ast
from typing import List, Dict, Optional

class ProjectAnalyzer:
    """
    Analyzes a Python project:
    - Indexes Python files
    - Extracts imports, functions, and classes using AST
    """

    EXCLUDED_DIRS = {"venv", "__pycache__", ".git", "site-packages"}

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.files: List[str] = []

    def build_file_index(self) -> List[str]:
        """
        Recursively collect all Python files in project.
        """

        self.files = [] # Reset to avoid duplication

        for root, dirs, files in os.walk(self.root_path):

            # Filter directories in-place
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self.files.append(full_path)
        
        return list(set(self.files)) # deduplicate
    
    def parse_file(self, file_path: str) -> Optional[ast.AST]:
        """
        Parse a Python file into AST.

        Returns:
            AST tree or None if parsing fails
        """

        try:
            with open(file_path, "r") as f:
                return ast.parse(f.read())
        except Exception:
            return None 
    
    def extract_metadata(self, file_path: str) -> Dict:
        """
        Extract imports, functions, and classes from a file.
        """

        tree = self.parse_file(file_path)
        if not tree:
            return {}
        
        imports = []
        functions = []
        classes = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            
        return {
            "imports": list(set(imports)),
            "functions": functions,
            "classes": classes
        }
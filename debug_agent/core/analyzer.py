import os
import ast
from typing import List

class ProjectAnalyzer:

    def __init__(self, root_path: str):
        self.root_path = root_path
        self.files: List[str] = []

    def build_file_index(self) -> List[str]:
        """
        Recursively index all python files
        """
        EXCLUDED_DIRS = {"venv", "__pycache__", ".git", "site-packages"}

        for root, dirs, files in os.walk(self.root_path):

            # remove unwanted dirs in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self.files.append(full_path)
        
        return self.files
    
    def parse_file(self, file_path: str):
        """
        Parse Python file using AST
        """
        with open(file_path, "r") as f:
            try:
                tree = ast.parse(f.read())
            except Exception:
                return None
        return tree    
    
    def extract_metadata(self, file_path: str):
        """
        Extract imports, functions, classes
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
                module = node.module or ""
                imports.append(module)
            
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            
        return {
            "imports": imports,
            "functions": functions,
            "classes": classes
        }
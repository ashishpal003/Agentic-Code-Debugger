import os
from typing import List, Dict


class ContextBuilder:
    """
    Builds relevant debugging context from:
    - Traceback
    - Project files
    """

    MAX_FILES = 5
    SNIPPET_WINDOW = 3
    MAX_SNIPPET_LINES = 20

    def __init__(self, files: List[str], logger):
        self.files = files
        self.logger = logger

    def is_valid_project_file(self, file_path: str) -> bool:
        return "site-packages" not in file_path and "venv" not in file_path

    def get_relevant_files(self, traceback_data):
        """
        Match traceback files with project files.
        """

        relevant = []

        for entry in traceback_data:
            tb_file = os.path.basename(entry["file"])

            for file in self.files:
                if not self.is_valid_project_file(file):
                    continue

                if os.path.basename(file) == tb_file:
                    relevant.append(file)

        return list(set(relevant))
    
    def load_code(self, files: List[str]) -> Dict[str, str]:
        """
        Load full file contents.
        """

        code_map = {}

        for file in files:
            try:
                with open(file, "r") as f:
                    code_map[file] = f.read()
            
            except Exception:
                continue
        
        return code_map
    
    def extract_snippet(self, file_path: str, line: int) -> str:
        """
        Extract focused snippet around error line.
        """

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            start = max(0, line - self.SNIPPET_WINDOW - 1)
            end = min(len(lines), line + self.SNIPPET_WINDOW)

            snippet = lines[start:end]
            return "".join(snippet[:self.MAX_SNIPPET_LINES])
        
        except Exception:
            return ""
    
    def rank_files(self, files: List[str], traceback_data: List[Dict]) -> List[str]:
        """
        Rank files based on traceback order.
        """

        def rank(file):
            for i, t in enumerate(traceback_data):
                if os.path.basename(file) in t["file"]:
                    return i
            return 999
        
        return sorted(files, key=rank)
    
    def build(self, traceback_data):
        """
        Build final context for LLM.
        """

        relevant_files = self.get_relevant_files(traceback_data)

        # Limit context size
        relevant_files = relevant_files[:self.MAX_FILES]

        code_map = self.load_code(relevant_files)

        snippets = {}

        for entry in traceback_data:
            tb_file = os.path.basename(entry['file'])
            line = entry["line"]

            for file in relevant_files:
                if os.path.basename(file) == tb_file:
                    snippets[file] = {
                        "line": line,
                        "snippet": self.extract_snippet(file, line)
                    }

        # Rank files
        relevant_files = self.rank_files(relevant_files, traceback_data)

        self.logger.log(
            message="Context built",
            relevant_files=relevant_files
        )

        return {
            "relevant_files": relevant_files,
            "code": code_map,
            "snippets": snippets
        }
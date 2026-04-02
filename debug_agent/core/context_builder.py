import os

class ContextBuilder:

    def __init__(self, files):
        self.files = files

    # def get_relevant_files(self, traceback_data):
    #     relevant = []

    #     for entry in traceback_data:
    #         for file in self.files:
    #             if entry["file"] in file:
    #                 relevant.append(file)
        
    #     return list(set(relevant))

    def get_relevant_files(self, traceback_data):
        relevant = []

        for entry in traceback_data:
            traceback_file = os.path.basename(entry["file"])

            for file in self.files:
                if os.path.basename(file) == traceback_file:
                    relevant.append(file)

        return list(set(relevant))
    
    def load_code(self, files):
        code_map = {}

        for file in files:
            try:
                with open(file, "r") as f:
                    code_map[file] = f.read()
            except Exception:
                continue
        
        return code_map
    
    def build(self, traceback_data):
        relevant_files = self.get_relevant_files(traceback_data)

        code_map = self.load_code(relevant_files)

        snippets = {}

        for entry in traceback_data:
            traceback_file = os.path.basename(entry['file'])
            line = entry["line"]

            for file in relevant_files:
                if os.path.basename(file) == traceback_file:
                    snippet = self.extract_snippet(file, line)

                    snippets[file] = {
                        "line": line,
                        "snippet": snippet
                    }

        return {
            "relevant_files": relevant_files,
            "code": code_map,
            "snippets": snippets
        }
    
    def extract_snippet(self, file, line, window=3):
        try:
            with open(file, "r") as f:
                lines = f.readlines()

            start = max(0, line-window-1)
            end = min(len(lines), line+window)

            return "".join(lines[start:end])
        except Exception:
            return ""
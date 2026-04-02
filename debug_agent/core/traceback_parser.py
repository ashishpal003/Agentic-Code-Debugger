import re

class TracebackParser:

    FILE_LINE_REGEX = r'File "(.+?)", line (\d+)'

    def parse(self, traceback: str):
        """
        Extract file paths and line numbers from traceback
        """
        matches = re.findall(self.FILE_LINE_REGEX, traceback)

        parsed = []
        for file, line in matches:
            parsed.append({
                "file": file,
                "line": int(line)
            })

        return parsed

if __name__ == "__main__":
    traceback = TracebackParser().parse('File "/app/main.py", line 10, in <module>')
    print(traceback)
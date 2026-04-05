import re
from typing import List, Dict


class TracebackParser:
    """
    Parse Python traceback to extract file paths and line numbers.
    """

    FILE_LINE_REGEX = r'File "(.+?)", line (\d+)'

    def parse(self, traceback: str) -> List[Dict]:
        matches = re.findall(self.FILE_LINE_REGEX, traceback)

        return [
            {"file": file, "line": int(line)}
            for file, line in matches
        ]
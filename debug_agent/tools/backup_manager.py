import os

class BackupManager:
    """
    Handles backup and restoration of files before applying patches.
    """

    def __init__(self):
        self.backups = {}

    def create_backup(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                self.backups[file_path] = f.read()

        except Exception:
            pass

    def restore(self, file_path: str):
        if file_path in self.backups:
            with open(file_path, "w") as f:
                f.write(self.backups[file_path])
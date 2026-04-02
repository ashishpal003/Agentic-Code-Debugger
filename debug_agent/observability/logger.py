import logging
import json
from datetime import datetime

class Logger:

    def __init__(self):
        self.logger = logging.getLogger("debug-agent")
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log(self, level="info", message="", **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }

        if level == "error":
            self.logger.error(json.dumps(log_entry))
        else:
            self.logger.info(json.dumps(log_entry))
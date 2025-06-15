"""
Logging utility for AutoTestUtility.
"""

import threading


class Logger:
    """
    Logging utility for AutoTestUtility.
    """

    def __init__(self, callback=None):
        self.entries = []
        self.callback = callback
        self._lock = threading.Lock()

    def log(self, message):
        """
        Record a log entry and invoke callback if provided.
        """
        with self._lock:
            self.entries.append(message)
        if self.callback:
            self.callback(message)

    def export(self, file_path):
        """
        Export all log entries to the given file path.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(entry + '\n')
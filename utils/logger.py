from datetime import datetime
from typing import List


class AgentLogger:
    """Simple in-memory logger (no Streamlit dependency)."""

    def __init__(self):
        self._logs: List[str] = []

    def log(self, agent: str, message: str):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] [{agent}] {message}"
        self._logs.append(entry)
        print(entry)          # also visible in terminal

    def get_logs(self) -> List[str]:
        return list(self._logs)

    def clear(self):
        self._logs.clear()
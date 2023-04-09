import logging
import sqlite3
import datetime as dt
from pathlib import Path


class CustomLogger:
    def __init__(self, log_level=logging.DEBUG, log_path=None, task_name=None, task_id=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # File handler
        if log_path is None and (task_name is None or task_id is None):
            raise ValueError("Either the log path or (task_name and task_id) must be provided.")

        if task_name is not None and task_id is not None:
            self.task_name = task_name
            self.task_id = task_id
            log_dir = Path('/nas_dir') / task_name / task_id
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = f"{task_id}.log"
            log_path = log_dir / log_filename
        else:
            self.task_name = None
            self.task_id = None
            log_path = Path('/nas_dir') / log_path

        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # SQLite handler
        self.db_path = log_path.with_suffix('.db')
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                             (timestamp TEXT, level TEXT, task_name TEXT, task_id TEXT, message TEXT)''')
        self.conn.commit()

    def log(self, level, message, task_name=None, task_id=None):
        self.logger.log(level, message)

        timestamp = str(dt.datetime.now())
        self.cursor.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", (timestamp, logging.getLevelName(level), task_name, task_id, message))
        self.conn.commit()

    def debug(self, message, task_name=None, task_id=None):
        self.log(logging.DEBUG, message, task_name, task_id)

    def info(self, message, task_name=None, task_id=None):
        self.log(logging.INFO, message, task_name, task_id)

    def warning(self, message, task_name=None, task_id=None):
        self.log(logging.WARNING, message, task_name, task_id)

    def error(self, message, task_name=None, task_id=None):
        self.log(logging.ERROR, message, task_name, task_id)

    def critical(self, message, task_name=None, task_id=None):
        self.log(logging.CRITICAL, message, task_name, task_id)

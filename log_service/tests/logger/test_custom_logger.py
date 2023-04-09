from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import unittest
import logging
import sqlite3

from log_service.logger.custom_logger import CustomLogger


class TestCustomLogger(unittest.TestCase):

    def setUp(self):
        # Set up the logger with test settings
        self.logger = CustomLogger(log_level=logging.DEBUG, log_path='test_log_path')

    def test_console_log(self):
        # Test that logging to console works
        expected_output = 'test message'
        with self.assertLogs(logger=self.logger.logger, level=logging.INFO) as cm:
            self.logger.info(expected_output)
        self.assertEqual(cm.output, [f'INFO:{__name__}:{expected_output}'])

    def test_file_log(self):
        # Test that logging to file works
        expected_output = 'test message'
        log_file_path = Path('/nas_path') / 'test_task' / 'test_id' / f"{self.logger.current_date}_test_id.log"
        with self.assertLogs(logger=self.logger.logger, level=logging.DEBUG):
            self.logger.debug(expected_output, task_name='test_task', task_id='test_id')
        with log_file_path.open() as f:
            self.assertIn(expected_output, f.read())

    def test_sqlite_log(self):
        # Test that logging to SQLite database works
        expected_output = 'test message'
        expected_timestamp = self.logger.get_current_time()
        expected_level = 'INFO'
        expected_task_name = 'test_task'
        expected_task_id = 'test_id'
        expected_message = expected_output
        self.logger.info(expected_output, task_name=expected_task_name, task_id=expected_task_id)
        conn = sqlite3.connect(str(self.logger.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE message=?", (expected_message,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], expected_timestamp)
        self.assertEqual(row[1], expected_level)
        self.assertEqual(row[2], expected_task_name)
        self.assertEqual(row[3], expected_task_id)
        self.assertEqual(row[4], expected_message)

    def tearDown(self):
        # Clean up the logger resources
        self.logger.conn.close()
        log_path = Path('/nas_path') / 'test_log_path.log'
        db_path = Path('/nas_path') / 'test_log_path.db'
        log_path.unlink(missing_ok=True)
        db_path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()

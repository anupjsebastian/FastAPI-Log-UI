import random
import string
from log_service.logger.custom_logger import CustomLogger
import logging

loggers = [
    CustomLogger(task_name=''.join(random.choices(string.ascii_letters, k=5)), task_id=str(random.randint(1, 100)))
    for _ in range(3)
]

log_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

for i in range(300):
    logger = random.choice(loggers)
    task_name = logger.task_name
    task_id = logger.task_id
    level = random.choice(log_levels)
    message = f"This is a {logging.getLevelName(level)} log message {i} for task {task_name}-{task_id}"
    logger.log(level, message, task_name, task_id)

import os
import sys
import logging

log_str = "[%(asctime)s: %(levelname)s: %(module)s: line %(lineno)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "site2brochure.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=log_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ],
    encoding='utf-8'
)

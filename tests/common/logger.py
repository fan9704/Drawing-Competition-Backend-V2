import logging
import os
from datetime import datetime


def setup_test_logger(name="test_logger", log_dir="logs"):
    """建立測試專用的 Logger"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 產生 log 檔名，例如 logs/test_20250315.log
    log_filename = f"{log_dir}/test_{datetime.now().strftime('%Y%m%d')}.log"

    # 設定 Logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 記錄所有等級的 Log

    # 設定 Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] - [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # 建立 File Handler
    file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 建立 Console Handler (讓測試時能即時看到 log)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 加入 Handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
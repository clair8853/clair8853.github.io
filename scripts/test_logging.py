import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.logger import setup_logging

def test_logging():
    logger = setup_logging()
    logger.info("Logging system test")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")

if __name__ == "__main__":
    test_logging()

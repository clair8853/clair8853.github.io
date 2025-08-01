import logging
import os
from datetime import datetime

def setup_logging():
    # 로그 디렉토리 생성
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 로그 파일명 설정 (날짜별)
    log_file = os.path.join(log_dir, f'mci_paper_{datetime.now().strftime("%Y%m%d")}.log')

    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

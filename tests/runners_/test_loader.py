# tests/runners/test_loader.py

import logging
from pathlib import Path

from scripts.pipeline import get_files

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        test_path = Path("tests/fixtures/test_docs")  # Change as needed
        logger.info(f"📁 Testing file loading from: {test_path}")

        files = get_files(test_path)
        logger.info(f"✅ Found {len(files)} supported files:")

        for f in files[:5]:
            print(f" - {f}")

    except Exception as e:
        logger.exception(f"❌ Loader test failed: {e}")

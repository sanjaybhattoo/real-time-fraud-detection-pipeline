import json
import logging
import os
import sys

from engine import FeatureEngine
from utils import setup_logging, wait_for_dependencies

logger = logging.getLogger(__name__)
setup_logging(os.getenv('LOG_LEVEL', 'INFO'))


def create_engine() -> 'FeatureEngine' or None:
    try:
        logger.info("Initializing Feature Engine...")
        engine = FeatureEngine()
        logger.info("Feature Engine initialized ")
        return engine
    except Exception as e:
        logger.error(f"Failed to initialize : {e}", exc_info=True)
        return None


def main():
    logger.info("=" * 80)
    logger.info("Feature Engine Service Starting")
    logger.info("=" * 80)
    if not wait_for_dependencies():
        logger.error("Dependencies not ready.")
        sys.exit(1)
    engine = create_engine()
    if not engine:
        logger.error("Failed to create engine.")
        sys.exit(1)
    try:
        logger.info("Starting feature loop...")
        engine.run()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Shutdown signal received")
    except Exception as e:
        logger.error(f" error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Cleaning up resources...")
        engine.cleanup()
        logger.info(" complete")


if __name__ == '__main__':
    main()

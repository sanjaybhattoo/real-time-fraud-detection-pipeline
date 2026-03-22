import json
import logging
import os
import sys

from predictor import FraudPredictor
from utils import setup_logging, wait_for_kafka

logger = logging.getLogger(__name__)
setup_logging(os.getenv('LOG_LEVEL', 'INFO'))


def create_predictor() -> 'FraudPredictor' or None:
    try:
        logger.info("Initializing Fraud Predictor...")
        predictor = FraudPredictor()
        logger.info("Fraud Predictor initialized successfully")
        return predictor
    except Exception as e:
        logger.error(f"Failed to initialize predictor: {e}", exc_info=True)
        return None


def main():
    logger.info("=" * 80)
    logger.info("Model Service Starting")
    logger.info("=" * 80)
  
    if not wait_for_kafka():
        logger.error("Kafka not ready. Exiting.")
        sys.exit(1)
    predictor = create_predictor()
    if not predictor:
        logger.error("Failed to create predictor. Exiting.")
        sys.exit(1)
    try:
        logger.info("Starting prediction...")
        predictor.run()
    except KeyboardInterrupt:
        logger.info("\nShutdown signal received")
    except Exception as e:
        logger.error(f" Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Cleaning up resources...")
        predictor.cleanup()
        logger.info("Shutdown complete")


if __name__ == '__main__':
    main()

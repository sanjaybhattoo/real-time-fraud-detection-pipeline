import logging
import time
import os
from datetime import datetime

import psycopg2
import redis
from confluent_kafka.admin import AdminClient


def setup_logging(level: str = 'INFO'):
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_timestamp(timestamp_str: str) -> datetime:
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))


def wait_for_dependencies(max_retries: int = 30, retry_delay: int = 2) -> bool:
  logger = logging.getLogger(__name__)
    
    # Get connection strings
    kafka_brokers = os.getenv('KAFKA_BROKERS', 'localhost:9092')
    pg_url = os.getenv('POSTGRES_URL')
    redis_url = os.getenv('REDIS_URL')
    
    # Check Kafka
    logger.info("Checking Kafka connection...")
    kafka_ready = False
    for i in range(max_retries):
        try:
            admin_client = AdminClient({
                'bootstrap.servers': kafka_brokers
            })
            admin_client.list_topics(timeout=5)
            logger.info("Kafka is ready")
            kafka_ready = True
            break
        except Exception as e:
            logger.warning(f"Kafka not ready (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    
    if not kafka_ready:
        logger.error(" Kafka failed to become ready")
        return False
    logger.info("Checking PostgreSQL connection...")
    pg_ready = False
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(pg_url)
            conn.close()
            logger.info("✅ PostgreSQL is ready")
            pg_ready = True
            break
        except Exception as e:
            logger.warning(f"PostgreSQL not ready (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    
    if not pg_ready:
        logger.error(" failed to become ready")
        return False
    logger.info("Checking Redis connection...")
    redis_ready = False
    for i in range(max_retries):
        try:
            r = redis.from_url(redis_url)
            r.ping()
            r.close()
            logger.info(" Redis is ready")
            redis_ready = True
            break
        except Exception as e:
            logger.warning(f" not ready (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    
    if not redis_ready:
        logger.error("failed")
        return False
    
    logger.info("=" * 60)
    logger.info("ready")
    logger.info("=" * 60)
    
    return True

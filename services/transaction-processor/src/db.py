
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import psycopg2
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class Database:
    """Database handler for PostgreSQL and MongoDB"""
    
    def __init__(self, postgres_url: str, mongo_url: str):
        """Initialize database connections"""
        self.postgres_url = postgres_url
        self.mongo_url = mongo_url
        
        # PostgreSQL
        try:
            self.pg_conn = psycopg2.connect(postgres_url)
            logger.info("PostgreSQL connected")
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
        
        # MongoDB
        try:
            self.mongo_client = MongoClient(mongo_url)
            self.mongo_db = self.mongo_client['fraud_db']
            self.mongo_client.admin.command('ping')
            logger.info("MongoDB connected")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    
    def insert_transaction(self, txn: Dict[str, Any]) -> None:
        """Insert transaction into PostgreSQL"""
        cursor = self.pg_conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO transactions 
                (transaction_id, user_id, card_id, merchant_id, amount, 
                 timestamp, ip_address, device_id, user_location, 
                 billing_address, shipping_address, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                txn['transaction_id'],
                txn['user_id'],
                txn['card_id'],
                txn['merchant_id'],
                float(txn['amount']),
                txn['timestamp'],
                txn.get('ip_address'),
                txn.get('device_id'),
                str(txn.get('user_location')),
                txn.get('billing_address'),
                txn.get('shipping_address'),
                str(txn)
            ))
            
            self.pg_conn.commit()
            logger.debug(f"Inserted transaction: {txn['transaction_id']}")
        
        except Exception as e:
            self.pg_conn.rollback()
            logger.error(f"Failed to insert transaction: {e}")
            raise
        
        finally:
            cursor.close()
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from MongoDB"""
        try:
            users_collection = self.mongo_db['users']
            profile = users_collection.find_one({'user_id': user_id})
            return profile
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return None
    
    def get_merchant_profile(self, merchant_id: str) -> Optional[Dict[str, Any]]:
        """Get merchant profile from MongoDB"""
        try:
            merchants_collection = self.mongo_db['merchants']
            profile = merchants_collection.find_one({'merchant_id': merchant_id})
            return profile
        except Exception as e:
            logger.error(f"Failed to get merchant profile: {e}")
            return None
    
    def close(self):
        """Close all connections"""
        if self.pg_conn:
            self.pg_conn.close()
            logger.info("PostgreSQL connection closed")
        
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB connection closed")

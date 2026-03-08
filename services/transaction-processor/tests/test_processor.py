import pytest
import json
from unittest.mock import Mock, patch, MagicMock

from src.processor import TransactionProcessor


class TestTransactionValidation:
    """Test transaction validation"""
    
    def test_valid_transaction(self, sample_transaction):
        """Test validation of valid transaction"""
        processor = TransactionProcessor.__new__(TransactionProcessor)
      
        
        is_valid, error = processor.validate_transaction(sample_transaction)
        
        assert is_valid is True
        assert error is None
    
    def test_missing_required_field(self, sample_transaction):
        """Test validation with missing required field"""
        processor = TransactionProcessor.__new__(TransactionProcessor)
        
        del sample_transaction['amount']
        is_valid, error = processor.validate_transaction(sample_transaction)
        
        assert is_valid is False
        assert error is not None
        assert 'amount' in error.lower()
    
    def test_negative_amount(self, sample_transaction):
        """Test validation with negative amount"""
        processor = TransactionProcessor.__new__(TransactionProcessor)
      
        sample_transaction['amount'] = -100
        
        is_valid, error = processor.validate_transaction(sample_transaction)
        
        assert is_valid is False
        assert 'positive' in error.lower()
    
    def test_invalid_timestamp(self, sample_transaction):
        """Test validation with invalid timestamp"""
      
        processor = TransactionProcessor.__new__(TransactionProcessor)
        sample_transaction['timestamp'] = 'not-a-date'
        
        is_valid, error = processor.validate_transaction(sample_transaction)
        
        assert is_valid is False


class TestProcessMessage:
    """Test message processing"""
    
    def test_valid_message_processing(self, sample_transaction):
        """Test processing a valid message"""
        processor = TransactionProcessor.__new__(TransactionProcessor)
        processor.db = Mock()
      
        processor.db.get_user_profile = Mock(return_value={'user_id': 'user_123'})
        processor.db.get_merchant_profile = Mock(return_value={'merchant_id': 'merchant_789'})
        processor.db.insert_transaction = Mock()
        processor.producer = Mock()
        processor.processed = 0
        processor.errors = 0
        
        msg = json.dumps(sample_transaction)
        result = processor.process_message(msg)
        
        assert result is True
    
    def test_invalid_json(self):
        """Test processing invalid JSON"""
        processor = TransactionProcessor.__new__(TransactionProcessor)
        processor.errors = 0
        
        result = processor.process_message("not-json")
        
        assert result is False

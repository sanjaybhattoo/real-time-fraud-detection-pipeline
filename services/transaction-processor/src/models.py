
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Transaction:
    """Transaction data model"""
    transaction_id: str
    user_id: str
    card_id: str
    merchant_id: str
    amount: float
    timestamp: str
    ip_address: str
    device_id: Optional[str] = None
    user_location: Optional[Dict[str, float]] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    merchant_profile: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'card_id': self.card_id,
            'merchant_id': self.merchant_id,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'ip_address': self.ip_address,
            'device_id': self.device_id,
            'user_location': self.user_location,
            'billing_address': self.billing_address,
            'shipping_address': self.shipping_address,
            'user_profile': self.user_profile,
            'merchant_profile': self.merchant_profile,
        }

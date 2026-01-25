#!/usr/bin/env python3
"""GET Routes for MoMo SMS Transaction API"""

import json
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse

class GetRoutes:
    def __init__(self, transactions: List[Dict[str, Any]]):
        self.transactions = transactions
        self.transactions_dict = {t['id']: t for t in transactions if t.get('id')}
    
    def handle_get_request(self, path: str) -> Tuple[int, Dict[str, Any]]:
        """
        Handle GET requests and return (status_code, response_data)
        """
        parsed_url = urlparse(path)
        route_path = parsed_url.path
        
        # Route: GET /transactions
        if route_path == '/transactions':
            return self._get_all_transactions()
        
        # Route: GET /transactions/{id}
        elif route_path.startswith('/transactions/') and len(route_path.split('/')) == 3:
            transaction_id = route_path.split('/')[-1]
            return self._get_transaction_by_id(transaction_id)
        
        # Route not found
        else:
            return 404, {"error": "Endpoint not found"}
    
    def _get_all_transactions(self) -> Tuple[int, Dict[str, Any]]:
        """
        GET /transactions - Return all transactions
        Returns: (200, {"data": transactions})
        """
        return 200, {
            "data": self.transactions,
            "count": len(self.transactions),
            "message": f"Retrieved {len(self.transactions)} transactions"
        }
    
    def _get_transaction_by_id(self, transaction_id: str) -> Tuple[int, Dict[str, Any]]:
        """
        GET /transactions/{id} - Return specific transaction
        Returns: (200, {"data": transaction}) or (404, {"error": "..."})
        """
        transaction = self.transactions_dict.get(transaction_id)
        
        if transaction:
            return 200, {
                "data": transaction,
                "message": f"Transaction {transaction_id} found"
            }
        else:
            return 404, {
                "error": "Transaction not found",
                "message": f"Transaction with ID '{transaction_id}' does not exist"
            }
    
    def update_transactions(self, transactions: List[Dict[str, Any]]):
        """Update the transactions data"""
        self.transactions = transactions
        self.transactions_dict = {t['id']: t for t in transactions if t.get('id')}

#!/usr/bin/env python3
"""REST API Server for MoMo SMS Transactions - GET Endpoints Focus"""

import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from routes_get import GetRoutes
from typing import Dict, List, Any

class TransactionAPI(BaseHTTPRequestHandler):
    # In-memory storage (loaded from JSON)
    transactions = []
    get_routes = None
    
    # Basic Auth credentials (username:password)
    VALID_CREDENTIALS = "admin:password123"
    
    def _authenticate(self) -> bool:
        """Check Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return False
            
        try:
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            return decoded_credentials == self.VALID_CREDENTIALS
        except:
            return False
    
    def _send_json_response(self, status_code: int, response_data: Dict[str, Any]):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        self.wfile.write(json.dumps(response_data, indent=2).encode())
    
    def _send_unauthorized(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized", "message": "Valid credentials required"}).encode())
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests using clean routing logic"""
        # Authentication check
        if not self._authenticate():
            self._send_unauthorized()
            return
        
        # Use GET routes handler
        if self.get_routes:
            status_code, response_data = self.get_routes.handle_get_request(self.path)
            self._send_json_response(status_code, response_data)
        else:
            self._send_json_response(500, {"error": "Server configuration error"})


def load_transactions():
    """Load transactions from JSON file and initialize GET routes"""
    try:
        with open('data/processed/transactions.json', 'r') as f:
            transactions = json.load(f)
            TransactionAPI.transactions = transactions
            TransactionAPI.get_routes = GetRoutes(transactions)
            print(f"[OK] Loaded {len(transactions)} transactions")
            print(f"[OK] Initialized GET routes handler")
    except FileNotFoundError:
        print("[WARNING] No transactions file found. Run 'python run_tests.py' first.")
        TransactionAPI.transactions = []
        TransactionAPI.get_routes = GetRoutes([])

def run_server(port=8080):
    """Run the API server with GET endpoints focus"""
    load_transactions()
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, TransactionAPI)
    
    print(f"\n=== MoMo API Server (GET Endpoints) ===")
    print(f"Server running on: http://localhost:{port}")
    print(f"\nAvailable GET Endpoints:")
    print(f"  GET /transactions        - List all transactions")
    print(f"  GET /transactions/{{id}}  - Get specific transaction")
    print(f"\nAuthentication: Basic Auth")
    print(f"  Username: admin")
    print(f"  Password: password123")
    print(f"\nHTTP Status Codes:")
    print(f"  200 OK - Successful request")
    print(f"  401 Unauthorized - Invalid credentials")
    print(f"  404 Not Found - Resource not found")
    print(f"\nTest with: curl -u admin:password123 -X GET http://localhost:{port}/transactions")
    print(f"\nPress Ctrl+C to stop server...\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] Server stopped gracefully.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

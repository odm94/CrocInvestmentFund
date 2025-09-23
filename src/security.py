"""
Security utilities for CROC Investment Fund
"""

import streamlit as st
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class RateLimiter:
    """Simple rate limiter for Streamlit apps"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def is_allowed(self, user_id: str = "default") -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        
        # Clean old requests
        self.requests = [
            req_time for req_time in self.requests 
            if now - req_time < timedelta(seconds=self.time_window)
        ]
        
        # Check if under limit
        if len(self.requests) >= self.max_requests:
            return False
        
        # Add current request
        self.requests.append(now)
        return True
    
    def get_wait_time(self) -> int:
        """Get seconds to wait before next request"""
        if not self.requests:
            return 0
        
        oldest_request = min(self.requests)
        wait_until = oldest_request + timedelta(seconds=self.time_window)
        wait_seconds = (wait_until - datetime.now()).total_seconds()
        
        return max(0, int(wait_seconds))

def validate_stock_symbol(symbol: str) -> bool:
    """Validate stock symbol input"""
    if not symbol:
        return False
    
    # Basic validation
    if len(symbol) > 10:
        return False
    
    # Check for dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
    if any(char in symbol for char in dangerous_chars):
        return False
    
    # Check if alphanumeric (with some exceptions)
    if not symbol.replace('.', '').replace('-', '').isalnum():
        return False
    
    return True

def log_security_event(event_type: str, details: str):
    """Log security events (in production, use proper logging)"""
    timestamp = datetime.now().isoformat()
    print(f"[SECURITY] {timestamp} - {event_type}: {details}")

def check_suspicious_activity(symbol: str, user_ip: str = "unknown") -> bool:
    """Check for suspicious activity patterns"""
    # Simple checks - in production, use more sophisticated detection
    
    # Check for SQL injection attempts
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION']
    if any(keyword in symbol.upper() for keyword in sql_keywords):
        log_security_event("SQL_INJECTION_ATTEMPT", f"Symbol: {symbol}, IP: {user_ip}")
        return True
    
    # Check for script injection attempts
    script_keywords = ['<script', 'javascript:', 'onload=', 'onerror=']
    if any(keyword in symbol.lower() for keyword in script_keywords):
        log_security_event("SCRIPT_INJECTION_ATTEMPT", f"Symbol: {symbol}, IP: {user_ip}")
        return True
    
    return False

# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=20, time_window=60)  # 20 requests per minute

def apply_security_checks(symbol: str) -> tuple[bool, str]:
    """Apply all security checks and return (is_allowed, message)"""
    
    # Validate input
    if not validate_stock_symbol(symbol):
        return False, "Invalid stock symbol format"
    
    # Check for suspicious activity
    if check_suspicious_activity(symbol):
        return False, "Suspicious activity detected"
    
    # Check rate limiting
    if not rate_limiter.is_allowed():
        wait_time = rate_limiter.get_wait_time()
        return False, f"Rate limit exceeded. Please wait {wait_time} seconds."
    
    return True, "OK"

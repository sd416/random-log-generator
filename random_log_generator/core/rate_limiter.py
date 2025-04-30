"""
Rate limiter module for Random Log Generator.

This module implements the token bucket algorithm for rate limiting log generation.
"""

import threading
import time


class TokenBucket:
    """
    Token bucket implementation for rate limiting.
    
    This class implements the token bucket algorithm, which is used to control the rate
    of log generation. Tokens are added to the bucket at a constant rate, and consumed
    when logs are generated. If there are not enough tokens in the bucket, log generation
    is paused until more tokens are available.
    
    Attributes:
        rate (float): Tokens added per second.
        capacity (float): Maximum number of tokens in the bucket.
        tokens (float): Current number of tokens in the bucket.
        timestamp (float): Timestamp of the last token update.
        lock (threading.Lock): Lock for thread safety.
    """
    
    def __init__(self, rate, capacity):
        """
        Initialize the TokenBucket with a given rate and capacity.
        
        Args:
            rate (float): Tokens added per second.
            capacity (float): Maximum number of tokens in the bucket.
        """
        self.rate = rate  # tokens added per second
        self.capacity = capacity  # max tokens in the bucket
        self.tokens = capacity
        self.timestamp = time.time()
        self.lock = threading.Lock()
    
    def consume(self, tokens):
        """
        Consume tokens from the bucket in a thread-safe manner.
        
        Args:
            tokens (float): Number of tokens to consume.
            
        Returns:
            bool: True if tokens were consumed, False if there were not enough tokens.
        """
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.timestamp
            self.tokens += elapsed * self.rate
            if self.tokens > self.capacity:
                self.tokens = self.capacity
            self.timestamp = current_time
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
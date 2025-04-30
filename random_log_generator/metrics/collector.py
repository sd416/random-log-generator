"""
Metrics collector module for Random Log Generator.

This module implements the Metrics class for collecting and reporting metrics about log generation.
"""

import statistics
import threading
import time


class Metrics:
    """
    Metrics collector for log generation.
    
    This class collects metrics about log generation, such as the total number of logs
    generated, the total number of bytes written, and the log generation rate.
    
    Attributes:
        total_logs (int): Total number of logs generated.
        total_bytes (int): Total number of bytes written.
        rates (list): List of log generation rates (in MB/s).
        start_time (float): Timestamp when metrics collection started.
        lock (threading.Lock): Lock for thread safety.
    """
    
    def __init__(self):
        """Initialize the Metrics with default values."""
        self.total_logs = 0
        self.total_bytes = 0
        self.rates = []
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def update(self, logs, bytes_written):
        """
        Update the metrics with the given logs and bytes in a thread-safe manner.
        
        Args:
            logs (int): Number of logs generated.
            bytes_written (int): Number of bytes written.
        """
        with self.lock:
            self.total_logs += logs
            self.total_bytes += bytes_written
            duration = time.time() - self.start_time
            if duration > 0:
                self.rates.append(bytes_written / duration / 1024 / 1024)  # MB/s
    
    def get_stats(self):
        """
        Get the current statistics in a thread-safe manner.
        
        Returns:
            dict: Dictionary containing the current statistics.
        """
        with self.lock:
            duration = time.time() - self.start_time
            avg_rate = statistics.mean(self.rates) if self.rates else 0
            max_rate = max(self.rates) if self.rates else 0
            min_rate = min(self.rates) if self.rates else 0
        return {
            "total_logs": self.total_logs,
            "total_bytes": self.total_bytes,
            "duration": duration,
            "avg_rate_mb_s": avg_rate,
            "max_rate_mb_s": max_rate,
            "min_rate_mb_s": min_rate
        }
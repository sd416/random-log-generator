"""
Base formatter module for Random Log Generator.

This module defines the abstract base class for log formatters.
"""

from abc import ABC, abstractmethod


class LogFormatter(ABC):
    """
    Abstract base class for log formatters.
    
    This class defines the interface for log formatters, which are responsible for
    formatting log entries in different formats.
    """
    
    @abstractmethod
    def format_log(self, timestamp, log_level, message, **kwargs):
        """
        Format a log entry.
        
        Args:
            timestamp (str): Timestamp for the log entry.
            log_level (str): Log level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
            message (str): Log message.
            **kwargs: Additional keyword arguments for formatting.
            
        Returns:
            str: Formatted log entry.
        """
        pass
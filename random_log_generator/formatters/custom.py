"""
Custom formatter module for Random Log Generator.

This module implements the custom log formatter, which formats log entries using a
user-defined format string.
"""

import string
import logging
from random_log_generator.formatters.base import LogFormatter


class CustomFormatter(LogFormatter):
    """
    Custom log formatter.
    
    This class formats log entries using a user-defined format string with placeholders
    that are replaced with actual values.
    
    Attributes:
        format_template (string.Template): Template for formatting log entries.
        app_names (list): List of application names to include in logs.
    """
    
    def __init__(self, format_string, app_names=None):
        """
        Initialize the custom formatter with a format string and optional app names.
        
        Args:
            format_string (str): Format string with placeholders for log entry values.
            app_names (list, optional): List of application names to include in logs.
        """
        self.format_template = string.Template(format_string)
        self.app_names = app_names or []
    
    def format_log(self, timestamp, log_level, message, **kwargs):
        """
        Format a log entry using the custom format string.
        
        Args:
            timestamp (str): Timestamp for the log entry.
            log_level (str): Log level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
            message (str): Log message.
            **kwargs: Additional keyword arguments for formatting.
            
        Returns:
            str: Formatted log entry.
        """
        # Add app name to message if app_names is provided
        if self.app_names:
            import random
            app_name = random.choice(self.app_names)
            message = f"{app_name}: {message}"
        
        # Create a dictionary with all available values for substitution
        values = {
            'timestamp': timestamp,
            'log_level': log_level,
            'message': message,
        }
        
        # Add any additional keyword arguments
        values.update(kwargs)
        
        try:
            # Substitute placeholders with actual values
            return self.format_template.substitute(values)
        except KeyError as e:
            logging.error(f"Missing key {e} in custom format. Using default format.")
            return f"{timestamp}, {log_level}, {message}"
        except Exception as e:
            logging.error(f"Error formatting log line: {e}. Using default format.")
            return f"{timestamp}, {log_level}, {message}"
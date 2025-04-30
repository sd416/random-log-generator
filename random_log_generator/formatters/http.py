"""
HTTP formatter module for Random Log Generator.

This module implements the HTTP log formatter, which formats log entries in HTTP log format.
"""

from random_log_generator.formatters.base import LogFormatter
from random_log_generator.utils.ip_generator import generate_ip_address
from random_log_generator.utils.user_agents import generate_random_user_agent


class HTTPFormatter(LogFormatter):
    """
    HTTP log formatter.
    
    This class formats log entries in HTTP log format, including IP address, user agent,
    HTTP status code, and message.
    
    Attributes:
        status_codes (dict): Dictionary mapping HTTP status codes to lists of messages.
    """
    
    def __init__(self, status_codes):
        """
        Initialize the HTTP formatter with a dictionary of status codes and messages.
        
        Args:
            status_codes (dict): Dictionary mapping HTTP status codes to lists of messages.
        """
        self.status_codes = status_codes
        self.status_code_list = list(status_codes.keys())
    
    def format_log(self, timestamp, log_level, message=None, **kwargs):
        """
        Format a log entry in HTTP log format.
        
        Args:
            timestamp (str): Timestamp for the log entry.
            log_level (str): Log level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR').
            message (str, optional): Log message. If not provided, a random message will be selected.
            **kwargs: Additional keyword arguments for formatting.
                ip_address (str, optional): IP address for the log entry.
                user_agent (str, optional): User agent for the log entry.
                status_code (str, optional): HTTP status code for the log entry.
            
        Returns:
            str: Formatted log entry.
        """
        # Get or generate IP address
        ip_address = kwargs.get('ip_address', generate_ip_address())
        
        # Get or generate user agent
        user_agent = kwargs.get('user_agent', generate_random_user_agent())
        
        # Get or select random status code
        status_code = kwargs.get('status_code')
        if status_code is None and self.status_code_list:
            import random
            status_code = random.choice(self.status_code_list)
        
        # Get or select random message for the status code
        if message is None and status_code in self.status_codes:
            import random
            messages = self.status_codes[status_code]
            if messages:
                message = random.choice(messages)
        
        # Default message if none is provided or selected
        if message is None:
            message = "Request processed"
        
        # Format the log entry
        return f"{timestamp} {log_level} {ip_address} - \"{user_agent}\" HTTP/1.1 {status_code} {message}"
"""
Console output handler module for Random Log Generator.

This module implements the console output handler, which writes log entries to the console.
"""

import logging
from random_log_generator.output.base import OutputHandler


class ConsoleOutputHandler(OutputHandler):
    """
    Console output handler.
    
    This class writes log entries to the console (stdout).
    """
    
    def __init__(self):
        """
        Initialize the console output handler.
        """
        logging.info("Initialized console output handler")
    
    def write(self, log_lines):
        """
        Write log lines to the console.
        
        Args:
            log_lines (list): List of log lines to write.
            
        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        try:
            print('\n'.join(log_lines))
            return True
        except Exception as e:
            logging.error(f"Error writing to console: {e}")
            return False
    
    def close(self):
        """
        Close the console output handler.
        
        This is a no-op for the console output handler, as there are no resources to release.
        """
        pass
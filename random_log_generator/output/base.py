"""
Base output handler module for Random Log Generator.

This module defines the abstract base class for output handlers.
"""

from abc import ABC, abstractmethod


class OutputHandler(ABC):
    """
    Abstract base class for output handlers.
    
    This class defines the interface for output handlers, which are responsible for
    writing log entries to different destinations, such as files or the console.
    """
    
    @abstractmethod
    def write(self, log_lines):
        """
        Write log lines to the output destination.
        
        Args:
            log_lines (list): List of log lines to write.
            
        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Close the output handler and release any resources.
        
        This method should be called when the output handler is no longer needed.
        """
        pass
"""
File output handler module for Random Log Generator.

This module implements the file output handler, which writes log entries to a file.
"""

import os
import logging
from random_log_generator.output.base import OutputHandler
from random_log_generator.output.rotation import rotate_log_file


class FileOutputHandler(OutputHandler):
    """
    File output handler.
    
    This class writes log entries to a file, with optional log rotation.
    
    Attributes:
        file_path (str): Path to the log file.
        file_handle (file): File handle for the log file.
        rotation_enabled (bool): Whether log rotation is enabled.
        rotation_size (int): Size threshold for log rotation in MB.
    """
    
    def __init__(self, file_path, rotation_enabled=False, rotation_size=10):
        """
        Initialize the file output handler.
        
        Args:
            file_path (str): Path to the log file.
            rotation_enabled (bool, optional): Whether log rotation is enabled.
            rotation_size (int, optional): Size threshold for log rotation in MB.
        """
        self.file_path = file_path
        self.rotation_enabled = rotation_enabled
        self.rotation_size = rotation_size
        self.file_handle = None
        
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Open the file in append mode
            self.file_handle = open(file_path, 'a')
            logging.info(f"Opened log file: {file_path}")
        except (IOError, OSError) as e:
            logging.error(f"Error opening log file {file_path}: {e}")
            raise
    
    def write(self, log_lines):
        """
        Write log lines to the file.
        
        Args:
            log_lines (list): List of log lines to write.
            
        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        if not self.file_handle:
            logging.error("File handle is not open")
            return False
        
        try:
            # Check if rotation is needed
            if self.rotation_enabled and self.file_handle.tell() >= self.rotation_size * 1024 * 1024:
                self.file_handle.close()
                self.file_handle = rotate_log_file(self.file_path)
            
            # Write log lines to the file
            self.file_handle.write('\n'.join(log_lines) + '\n')
            self.file_handle.flush()
            return True
        except (IOError, OSError) as e:
            logging.error(f"Error writing to log file {self.file_path}: {e}")
            return False
    
    def close(self):
        """
        Close the file handle.
        """
        if self.file_handle:
            try:
                self.file_handle.close()
                logging.info(f"Closed log file: {self.file_path}")
            except (IOError, OSError) as e:
                logging.error(f"Error closing log file {self.file_path}: {e}")
            finally:
                self.file_handle = None
"""
Log rotation module for Random Log Generator.

This module provides functions for rotating log files.
"""

import os
import logging
import datetime


def rotate_log_file(log_file_path):
    """
    Rotate the log file by renaming the current log file and creating a new one.
    
    Args:
        log_file_path (str): Path to the log file to rotate.
        
    Returns:
        file: File handle for the new log file.
        
    Raises:
        IOError: If there is an error creating the new log file.
        OSError: If there is an error renaming the old log file.
    """
    # Generate a timestamp for the rotated file name
    base, ext = os.path.splitext(log_file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rotated_log_file_path = f"{base}_{timestamp}{ext}"
    
    # Rename the current log file if it exists
    if os.path.exists(log_file_path):
        try:
            os.rename(log_file_path, rotated_log_file_path)
            logging.info(f"Rotated log file to: {rotated_log_file_path}")
        except OSError as e:
            logging.error(f"Error rotating log file {log_file_path}: {e}")
            raise
    else:
        logging.warning(f"Log file {log_file_path} does not exist. Skipping rotation.")
    
    # Create a new log file
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(log_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Open the new log file
        new_file = open(log_file_path, 'w')
        logging.info(f"Created new log file: {log_file_path}")
        return new_file
    except (IOError, OSError) as e:
        logging.error(f"Error creating new log file {log_file_path}: {e}")
        raise
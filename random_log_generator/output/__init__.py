"""
Output module for Random Log Generator.

This module contains classes for handling log output to different destinations,
such as files or the console, as well as log rotation functionality.
"""

from random_log_generator.output.base import OutputHandler
from random_log_generator.output.file_output import FileOutputHandler
from random_log_generator.output.console_output import ConsoleOutputHandler
from random_log_generator.output.rotation import rotate_log_file

__all__ = [
    'OutputHandler',
    'FileOutputHandler',
    'ConsoleOutputHandler',
    'rotate_log_file',
]
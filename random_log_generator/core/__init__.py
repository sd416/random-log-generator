"""
Core module for Random Log Generator.

This module contains the core functionality for generating logs, including rate limiting
and different generation strategies.
"""

from random_log_generator.core.generator import generate_log_line, write_logs # Added write_logs
from random_log_generator.core.rate_limiter import TokenBucket
from random_log_generator.core.strategies import (
    # write_logs, # Removed: write_logs is in generator.py
    write_logs_random_rate,
    write_logs_random_segments
)

__all__ = [
    'generate_log_line',
    'TokenBucket',
    'write_logs', # This name is now correctly sourced from .generator
    'write_logs_random_rate',
    'write_logs_random_segments',
]

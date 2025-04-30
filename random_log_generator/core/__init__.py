"""
Core module for Random Log Generator.

This module contains the core functionality for generating logs, including rate limiting
and different generation strategies.
"""

from random_log_generator.core.generator import generate_log_line
from random_log_generator.core.rate_limiter import TokenBucket
from random_log_generator.core.strategies import (
    write_logs,
    write_logs_random_rate,
    write_logs_random_segments
)

__all__ = [
    'generate_log_line',
    'TokenBucket',
    'write_logs',
    'write_logs_random_rate',
    'write_logs_random_segments',
]
"""
Random Log Generator - A tool for generating realistic log entries with configurable rates and formats.
"""

__version__ = '0.1.0'
__author__ = 'Random Log Generator Team'

from random_log_generator.core.generator import generate_log_line
from random_log_generator.core.rate_limiter import TokenBucket
from random_log_generator.metrics.collector import Metrics

__all__ = [
    'generate_log_line',
    'TokenBucket',
    'Metrics',
]
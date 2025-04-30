"""
Metrics module for Random Log Generator.

This module contains classes for collecting and reporting metrics about log generation,
such as total logs generated, bytes written, and generation rates.
"""

from random_log_generator.metrics.collector import Metrics
from random_log_generator.metrics.reporter import format_metrics

__all__ = [
    'Metrics',
    'format_metrics',
]
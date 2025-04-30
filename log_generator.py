#!/usr/bin/env python3
"""
Compatibility layer for Random Log Generator.

This module provides backward compatibility with the original log_generator.py script.
It imports and re-exports the necessary functions and classes from the new package structure.
"""

import logging
import sys
import warnings

# Show deprecation warning
warnings.warn(
    "Direct use of log_generator.py is deprecated. "
    "Please use the random_log_generator package instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import from the new package structure
from random_log_generator.core.generator import (
    generate_log_line,
    write_logs,
    main
)
from random_log_generator.core.strategies import (
    write_logs_random_rate,
    write_logs_random_segments
)
from random_log_generator.core.rate_limiter import TokenBucket
from random_log_generator.metrics.collector import Metrics
from random_log_generator.utils.ip_generator import generate_ip_address
from random_log_generator.utils.user_agents import (
    generate_random_user_agent,
    generate_random_user_agent_uncached
)
from random_log_generator.output.rotation import rotate_log_file
from random_log_generator.config.config_loader import load_config

# Re-export all the imported names
__all__ = [
    'generate_log_line',
    'write_logs',
    'write_logs_random_rate',
    'write_logs_random_segments',
    'TokenBucket',
    'Metrics',
    'generate_ip_address',
    'generate_random_user_agent',
    'generate_random_user_agent_uncached',
    'rotate_log_file',
    'main'
]

# Load configuration
try:
    config_data = load_config('config.yaml')
    CONFIG = config_data
except Exception as e:
    logging.error(f"Error loading configuration: {e}")
    sys.exit(1)

if __name__ == "__main__":
    # Run the main function with the loaded configuration
    sys.exit(main(CONFIG))

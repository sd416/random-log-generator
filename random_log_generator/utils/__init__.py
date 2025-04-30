"""
Utilities module for Random Log Generator.

This module contains utility functions for generating random data used in log entries,
such as user agents and IP addresses.
"""

from random_log_generator.utils.user_agents import generate_random_user_agent
from random_log_generator.utils.ip_generator import generate_ip_address

__all__ = [
    'generate_random_user_agent',
    'generate_ip_address',
]
"""
IP address generator module for Random Log Generator.

This module provides functions for generating random IP addresses.
"""

import ipaddress
import random


def generate_ip_address():
    """
    Generate a random IP address.
    
    Returns:
        str: A random IPv4 address as a string.
    """
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
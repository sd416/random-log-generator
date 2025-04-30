"""
User agent generator module for Random Log Generator.

This module provides functions for generating random user agents.
"""

import random


# These lists will be populated from the configuration
user_agent_browsers = []
user_agent_systems = []


def initialize_user_agents(browsers, systems):
    """
    Initialize the user agent generator with browser and system lists.
    
    Args:
        browsers (list): List of browser names.
        systems (list): List of operating system strings.
    """
    global user_agent_browsers, user_agent_systems
    user_agent_browsers = browsers
    user_agent_systems = systems


def generate_random_user_agent_uncached():
    """
    Generate a random user agent without caching.
    
    Returns:
        str: A random user agent string.
    """
    if not user_agent_browsers or not user_agent_systems:
        return "Mozilla/5.0 (Unknown) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124"
    
    browser = random.choice(user_agent_browsers)
    system = random.choice(user_agent_systems)
    version = {
        "Chrome": f"Chrome/{random.randint(70, 100)}.0.{random.randint(3000, 4000)}.124",
        "Firefox": f"Firefox/{random.randint(70, 100)}.0",
        "Safari": f"Safari/{random.randint(605, 610)}.1.15",
        "Edge": f"Edg/{random.randint(80, 100)}.0.{random.randint(800, 900)}.59",
        "Opera": f"Opera/{random.randint(60, 70)}.0.{random.randint(3000, 4000)}.80",
        "Brave": f"Brave Chrome/{random.randint(70, 100)}.0.{random.randint(3000, 4000)}.124",
    }
    
    browser_key = browser if browser in version else "Chrome"
    user_agent = f"Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) {version[browser_key]}"
    return user_agent


# Create a pool of pre-generated user agents
user_agent_pool = []


def initialize_user_agent_pool(size=100):
    """
    Initialize the user agent pool with a given number of pre-generated user agents.
    
    Args:
        size (int): Number of user agents to pre-generate.
    """
    global user_agent_pool
    user_agent_pool = [generate_random_user_agent_uncached() for _ in range(size)]


def generate_random_user_agent():
    """
    Select a random user agent from the pre-generated pool.
    
    Returns:
        str: A random user agent string.
    """
    if not user_agent_pool:
        return generate_random_user_agent_uncached()
    return random.choice(user_agent_pool)
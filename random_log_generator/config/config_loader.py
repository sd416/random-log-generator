"""
Configuration loader module for Random Log Generator.

This module provides functions for loading and parsing configuration from YAML files
and environment variables.
"""

import os
import yaml
import logging


def load_config(config_path='config.yaml'):
    """
    Load configuration from a YAML file.
    
    Args:
        config_path (str): Path to the configuration file.
        
    Returns:
        dict: Configuration dictionary.
        
    Raises:
        FileNotFoundError: If the configuration file is not found.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            logging.info(f"Configuration loaded from {config_path}")
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_path}' not found.")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing '{config_path}': {e}")
        raise
    
    # Extract configurations
    config = config_data.get('CONFIG', {})
    
    # Override with environment variables if present
    override_from_env(config)
    
    return config


def override_from_env(config):
    """
    Override configuration values with environment variables.
    
    Environment variables should be prefixed with 'LOG_GEN_' and be in uppercase.
    For example, 'LOG_GEN_DURATION_NORMAL' would override 'duration_normal'.
    
    Args:
        config (dict): Configuration dictionary to update.
    """
    prefix = 'LOG_GEN_'
    for key in list(config.keys()):
        env_key = f"{prefix}{key.upper()}"
        if env_key in os.environ:
            env_value = os.environ[env_key]
            
            # Try to convert to the same type as the original value
            original_type = type(config[key])
            try:
                if original_type == bool:
                    # Special handling for boolean values
                    config[key] = env_value.lower() in ('true', 'yes', '1', 'y')
                elif original_type == list:
                    # Split comma-separated values for lists
                    config[key] = [item.strip() for item in env_value.split(',')]
                else:
                    # For other types, use the constructor
                    config[key] = original_type(env_value)
                logging.info(f"Configuration '{key}' overridden from environment variable")
            except (ValueError, TypeError) as e:
                logging.warning(f"Could not convert environment variable {env_key} to {original_type.__name__}: {e}")
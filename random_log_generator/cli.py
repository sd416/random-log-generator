#!/usr/bin/env python3
"""
Command-line interface for Random Log Generator.

This module provides the entry point for the application, handling command-line arguments
and initializing the log generator with the appropriate configuration.
"""

import argparse
import logging
import sys
import time

from random_log_generator.config.config_loader import load_config
from random_log_generator.config.validators import validate_config
from random_log_generator.metrics.collector import Metrics


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate realistic log entries with configurable rates and formats.'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='Path to the configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information and exit'
    )
    return parser.parse_args()


def setup_logging(verbose=False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Show version and exit if requested
    if args.version:
        from random_log_generator import __version__
        print(f"Random Log Generator v{__version__}")
        return 0
    
    # Set up logging
    setup_logging(args.verbose)
    
    try:
        # Load and validate configuration
        config = load_config(args.config)
        validate_config(config)
        
        # Initialize metrics collector
        metrics = Metrics()
        
        # Import main function here to avoid circular imports
        from random_log_generator.core.generator import main as run_generator
        
        # Run the generator
        logging.info("Starting log generator...")
        run_generator(config, metrics)
        
        return 0
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        return 0
    except Exception as e:
        logging.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
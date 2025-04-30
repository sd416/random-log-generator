"""
Core generator module for Random Log Generator.

This module provides functions for generating log entries.
"""

import datetime
import logging
import random
import time
import threading

from random_log_generator.utils.ip_generator import generate_ip_address
from random_log_generator.utils.user_agents import (
    initialize_user_agents,
    initialize_user_agent_pool,
    generate_random_user_agent
)
from random_log_generator.formatters.http import HTTPFormatter
from random_log_generator.formatters.custom import CustomFormatter
from random_log_generator.core.rate_limiter import TokenBucket
from random_log_generator.metrics.collector import Metrics


def initialize_formatters(config, http_status_codes, log_levels):
    """
    Initialize the appropriate formatter based on configuration.
    
    Args:
        config (dict): Configuration dictionary.
        http_status_codes (dict): Dictionary of HTTP status codes and messages.
        log_levels (list): List of log levels.
        
    Returns:
        tuple: A tuple containing the formatter and log levels.
    """
    if config['http_format_logs']:
        formatter = HTTPFormatter(http_status_codes)
    else:
        formatter = CustomFormatter(
            config['custom_log_format'],
            config['custom_app_names']
        )
    
    return formatter, log_levels


def generate_log_line(formatter, log_levels):
    """
    Generate a single log line with a timestamp and realistic message.
    
    Args:
        formatter: The formatter to use for formatting the log line.
        log_levels (list): List of log levels to choose from.
        
    Returns:
        str: A formatted log line.
    """
    # Generate timestamp
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Select random log level
    log_level = random.choice(log_levels)
    
    # Generate a random message
    messages = [
        "User login successful",
        "Database query executed",
        "API request received",
        "File upload completed",
        "Cache updated",
        "Configuration loaded",
        "Session expired",
        "Data validation passed",
        "Background task started",
        "Email notification sent"
    ]
    message = random.choice(messages)
    
    # Format the log line using the formatter
    return formatter.format_log(timestamp, log_level, message)


def write_logs(rate, duration, output_handler, formatter, log_levels, metrics=None):
    """
    Write logs at a specified rate for a specified duration.
    
    Args:
        rate (float): Log generation rate in MB/s.
        duration (float): Duration to generate logs for in seconds.
        output_handler: The output handler to use for writing logs.
        formatter: The formatter to use for formatting log lines.
        log_levels (list): List of log levels to choose from.
        metrics (Metrics, optional): Metrics collector to update with statistics.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    logging.info(f"Writing logs at rate: {rate:.4f} MB/s for {duration:.2f} seconds")
    
    # Calculate tokens per second based on rate and log line size
    log_line_size = 100  # Approximate size of each log line in bytes
    tokens_per_second = rate * 1024 * 1024 / log_line_size
    
    # Initialize token bucket
    token_bucket = TokenBucket(tokens_per_second, tokens_per_second)
    
    # Calculate end time
    end_time = time.time() + duration
    
    # Initialize counters
    logs_written = 0
    bytes_written = 0
    
    # Initial batch size
    batch_size = 1024
    log_lines = []
    expected_batch_time = batch_size / tokens_per_second
    
    # Track time spent sleeping
    total_sleep_time = 0
    
    while time.time() < end_time:
        start_time = time.time()
        
        # Ensure batch_size is an integer
        batch_size = int(batch_size)
        
        if token_bucket.consume(batch_size):  # Check if we can write `batch_size` logs
            for _ in range(batch_size):
                log_line = generate_log_line(formatter, log_levels)
                log_lines.append(log_line)
                logs_written += 1
                bytes_written += len(log_line) + 1  # +1 for newline
            
            # Write log lines to the output handler
            if output_handler.write(log_lines):
                log_lines.clear()
            else:
                logging.error("Failed to write log lines to output handler")
                return False
            
            # Calculate the time taken to process this batch
            elapsed_time = time.time() - start_time
            sleep_time = max(0, expected_batch_time - elapsed_time)
            
            # Adjust batch size based on sleep time
            if sleep_time > 0:
                total_sleep_time += sleep_time
                # If we're spending too much time sleeping, increase the batch size
                if total_sleep_time > 0.05:  # Adjust this threshold as needed
                    batch_size = min(batch_size * 1.2, tokens_per_second)  # Ensure we don't exceed the rate
                    total_sleep_time = 0  # Reset the sleep tracker
                    logging.debug(f"Increasing batch size to: {int(batch_size)}")
            else:
                # If not sleeping, increase batch size more aggressively
                batch_size = min(batch_size * 1.5, tokens_per_second)
                logging.debug(f"Rapidly increasing batch size to: {int(batch_size)}")
            
            # Sleep if necessary
            time.sleep(sleep_time)
        else:
            time.sleep(0.05)  # Sleep for a short time if no tokens are available
    
    # Update metrics if provided
    if metrics:
        metrics.update(logs_written, bytes_written)
    
    return True


def main(config, metrics_instance=None):
    """
    Main function to initiate log writing based on configuration.
    
    Args:
        config (dict): Configuration dictionary.
        metrics_instance (Metrics, optional): Metrics collector to update with statistics.
        
    Returns:
        int: Exit code (0 for success, non-zero for failure).
    """
    # Load additional configuration data
    from random_log_generator.config.config_loader import load_config
    config_data = load_config()
    
    # Extract additional configuration
    log_levels = config_data.get('log_levels', ['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    http_status_codes = config_data.get('http_status_codes', {})
    user_agent_browsers = config_data.get('user_agent_browsers', [])
    user_agent_systems = config_data.get('user_agent_systems', [])
    
    # Initialize user agents
    initialize_user_agents(user_agent_browsers, user_agent_systems)
    initialize_user_agent_pool(100)
    
    # Initialize metrics collector if not provided
    if metrics_instance is None:
        metrics_instance = Metrics()
    
    # Initialize formatter
    formatter, log_levels = initialize_formatters(config, http_status_codes, log_levels)
    
    # Initialize output handler
    from random_log_generator.output.file_output import FileOutputHandler
    from random_log_generator.output.console_output import ConsoleOutputHandler
    
    if config['write_to_file']:
        try:
            output_handler = FileOutputHandler(
                config['log_file_path'],
                config['log_rotation_enabled'],
                config['log_rotation_size']
            )
        except (IOError, OSError) as e:
            logging.error(f"Error initializing file output handler: {e}")
            return 1
    else:
        output_handler = ConsoleOutputHandler()
    
    # Set up signal handlers for graceful shutdown
    start_time = time.time()
    iteration = 0
    interrupted = False
    
    def handle_interrupt(signal_received, frame):
        nonlocal interrupted
        interrupted = True
        logging.info("Interrupt received, shutting down...")
        logging.info(f"Final metrics: {metrics_instance.get_stats()}")
        output_handler.close()
        exit(0)
    
    # Import signal module here to avoid circular imports
    import signal
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    
    try:
        # Import strategies here to avoid circular imports
        from random_log_generator.core.strategies import (
            write_logs_random_segments,
            write_logs_random_rate
        )
        
        # Main log generation loop
        while config['stop_after_seconds'] == -1 or time.time() - start_time < config['stop_after_seconds']:
            # Normal period with random segments
            success = write_logs_random_segments(
                config['duration_normal'],
                5,  # Maximum segment duration
                config['rate_normal_min'],
                config['rate_normal_max'],
                config['base_exit_probability'],
                output_handler,
                formatter,
                log_levels,
                metrics_instance
            )
            
            if not success:
                logging.error("Failed during normal log generation period")
                break
            
            # Peak period with random rate
            success = write_logs_random_rate(
                config['duration_peak'],
                config['rate_normal_max'],
                config['rate_peak'],
                output_handler,
                formatter,
                log_levels,
                metrics_instance
            )
            
            if not success:
                logging.error("Failed during peak log generation period")
                break
            
            iteration += 1
            logging.info(f"Iteration {iteration} metrics: {metrics_instance.get_stats()}")
    except Exception as e:
        logging.error(f"An error occurred during log generation: {e}")
        return 1
    finally:
        if not interrupted:
            logging.info(f"Final metrics: {metrics_instance.get_stats()}")
        output_handler.close()
    
    return 0
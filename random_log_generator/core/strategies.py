"""
Strategies module for Random Log Generator.

This module provides different strategies for generating logs, such as random rates
and random segments.
"""

import logging
import random
import time

# Removed: from random_log_generator.core.generator import write_logs


def write_logs_random_rate(duration, rate_min, rate_max, output_handler, formatter, log_levels,
                          log_line_size_estimate, write_logs_func, metrics=None, 
                          rate_change_probability=0.2, rate_change_max_percentage=0.3):
    """
    Write logs at a random rate between rate_min and rate_max for a given duration.
    
    Args:
        duration (float): Duration to generate logs for in seconds.
        rate_min (float): Minimum log generation rate in MB/s.
        rate_max (float): Maximum log generation rate in MB/s.
        output_handler: The output handler to use for writing logs.
        formatter: The formatter to use for formatting log lines.
        log_levels (list): List of log levels to choose from.
        log_line_size_estimate (int): Estimated size of a single log line in bytes.
        write_logs_func (callable): The function to call for writing logs (e.g., core.generator.write_logs).
        metrics (Metrics, optional): Metrics collector to update with statistics.
        rate_change_probability (float, optional): Probability of changing the maximum log generation rate.
        rate_change_max_percentage (float, optional): Maximum percentage change in the log generation rate.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    end_time = time.time() + duration
    remaining_time = duration
    
    # Potentially change the maximum rate
    if random.random() < rate_change_probability:
        change_percentage = random.uniform(-rate_change_max_percentage, rate_change_max_percentage)
        rate_max *= (1 + change_percentage)
        logging.info(f"Changing rate_max by {change_percentage*100:.2f}%, new rate_max: {rate_max:.4f} MB/s")
    
    while remaining_time > 0:
        # Generate a random segment duration
        segment_duration = random.uniform(1, remaining_time)
        
        # Generate a random rate within the specified range
        rate = random.uniform(rate_min, rate_max)
        logging.info(f"Selected random rate: {rate:.4f} MB/s")
        
        # Write logs at the selected rate for the segment duration
        success = write_logs_func(rate, segment_duration, output_handler, formatter, log_levels, 
                                  log_line_size_estimate, metrics)
        if not success:
            return False
        
        # Update remaining time
        remaining_time -= segment_duration
    
    return True


def write_logs_random_segments(total_duration, segment_max_duration, rate_min, rate_max,
                              base_exit_probability, output_handler, formatter, log_levels,
                              log_line_size_estimate, write_logs_func, metrics=None):
    """
    Write logs in random segments with a chance to exit early.
    
    Args:
        total_duration (float): Total duration to generate logs for in seconds.
        segment_max_duration (float): Maximum duration of each segment in seconds.
        rate_min (float): Minimum log generation rate in MB/s.
        rate_max (float): Maximum log generation rate in MB/s.
        base_exit_probability (float): Base probability of exiting early during a logging segment.
        output_handler: The output handler to use for writing logs.
        formatter: The formatter to use for formatting log lines.
        log_levels (list): List of log levels to choose from.
        log_line_size_estimate (int): Estimated size of a single log line in bytes.
        write_logs_func (callable): The function to call for writing logs.
        metrics (Metrics, optional): Metrics collector to update with statistics.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    remaining_time = total_duration
    
    while remaining_time > 0:
        # Calculate exit probability with some variability
        exit_probability = base_exit_probability * random.uniform(0.5, 1.5)
        
        # Check if we should exit early
        if random.random() < exit_probability:
            logging.info("Exiting early based on random exit clause.")
            return True
        
        # Generate a random segment duration
        segment_duration = random.uniform(1, min(segment_max_duration, remaining_time))
        
        # Write logs at a random rate for the segment duration
        success = write_logs_random_rate(
            segment_duration, rate_min, rate_max,
            output_handler, formatter, log_levels, log_line_size_estimate, 
            write_logs_func, metrics
        )
        
        if not success:
            return False
        
        # Update remaining time
        remaining_time -= segment_duration
    
    return True

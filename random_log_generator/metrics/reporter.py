"""
Metrics reporter module for Random Log Generator.

This module provides functions for formatting metrics into human-readable strings.
"""


def format_metrics(metrics):
    """
    Format metrics into a human-readable string with rounded numbers.
    
    Args:
        metrics (dict): Dictionary containing metrics from Metrics.get_stats().
        
    Returns:
        str: Formatted metrics string.
    """
    total_mb = metrics['total_bytes'] / (1024 * 1024)  # Convert bytes to MB
    formatted_stats = (
        f"Total Logs: {metrics['total_logs']:,}, "
        f"Total Data: {total_mb:.3f} MB, "
        f"Duration: {metrics['duration']:.3f} seconds, "
        f"Average Rate: {metrics['avg_rate_mb_s']:.3f} MB/s, "
        f"Maximum Rate: {metrics['max_rate_mb_s']:.3f} MB/s, "
        f"Minimum Rate: {metrics['min_rate_mb_s']:.3f} MB/s"
    )
    return formatted_stats
import random
import time
import datetime

# Default configuration values
duration_normal = 120  # seconds
duration_peak = 4  # seconds
rate_normal_min = 0.0001  # MB/s
rate_normal_max = 1.1000  # MB/s
rate_peak = 1.2000  # MB/s
log_line_size = 100  # Average size of a log line in bytes
base_exit_probability = 0.12  # Base 12% chance to exit early
rate_change_probability = 0.3  # 30% chance to change rate_max
rate_change_max_percentage = 0.4  # Maximum 40% change in rate_max
write_to_file = True  # Flag to indicate if logs should be written to a file
log_file_path = 'logs.txt'  # File path for log output
http_format_logs = True  # Flag to format logs in HTTP response-like format
stop_after_seconds = -1  # Stop the script after X seconds (default -1 for continuous)
custom_app_names = []  # List of custom application names

log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
log_messages = [
    'User login successful',
    'User login failed',
    'Data fetched successfully',
    'Error fetching data from database',
    'User logged out',
    'Unexpected error occurred',
    'Service started',
    'Service stopped',
    'Configuration updated',
    'Permission denied',
    'File not found',
    'Connection timeout',
    'Data processed successfully',
    'Invalid user input detected',
    'Resource allocation failure',
    'Disk space running low',
    'Database connection established',
    'Database connection lost',
    'Cache cleared',
    'Cache update failed',
    'Scheduled task started',
    'Scheduled task completed',
    'Backup completed successfully',
    'Backup failed',
    'User session expired',
    'Session token refreshed',
    'New user registered',
    'Password change requested',
    'Password change successful',
    'Password change failed',
    'API request received',
    'API response sent',
    'Service health check passed',
    'Service health check failed',
    'Application deployment started',
    'Application deployment completed',
    'Application rollback initiated',
    'Application rollback completed',
    'Configuration validation error',
    'File uploaded successfully',
    'File upload failed',
    'User profile updated',
    'User profile update failed',
    'Email sent successfully',
    'Email delivery failed',
    'SMS sent successfully',
    'SMS delivery failed',
    'Payment transaction completed',
    'Payment transaction failed',
    'Credit card validation error',
    'User account locked',
    'User account unlocked'
]

http_status_codes = {
    '200 OK': ['User login successful', 'Data fetched successfully', 'User logged out', 'Service started', 'Service stopped', 'Configuration updated', 'Data processed successfully', 'Database connection established', 'Cache cleared', 'Scheduled task started', 'Scheduled task completed', 'Backup completed successfully', 'Session token refreshed', 'New user registered', 'Password change requested', 'Password change successful', 'API request received', 'API response sent', 'Service health check passed', 'Application deployment started', 'Application deployment completed', 'Application rollback initiated', 'Application rollback completed', 'File uploaded successfully', 'User profile updated', 'Email sent successfully', 'SMS sent successfully', 'Payment transaction completed', 'User account unlocked'],
    '400 Bad Request': ['Invalid user input detected', 'Configuration validation error', 'Credit card validation error'],
    '401 Unauthorized': ['User login failed', 'Permission denied'],
    '403 Forbidden': ['Permission denied'],
    '404 Not Found': ['File not found'],
    '500 Internal Server Error': ['Error fetching data from database', 'Unexpected error occurred', 'Resource allocation failure', 'Database connection lost', 'Cache update failed', 'Backup failed', 'Password change failed', 'Service health check failed', 'File upload failed', 'User profile update failed', 'Email delivery failed', 'SMS delivery failed', 'Payment transaction failed', 'User account locked']
}

def generate_log_line(http_format_logs=http_format_logs, custom_app_names=custom_app_names):
    """Generate a single log line with a timestamp and realistic message."""
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    log_level = random.choice(log_levels)
    message = random.choice(log_messages)
    
    if custom_app_names:
        app_name = random.choice(custom_app_names)
        message = f"{app_name}: {message}"
    
    if http_format_logs:
        for status_code, messages in http_status_codes.items():
            if message in messages:
                return f"{timestamp} {log_level} HTTP/1.1 {status_code} {message}"
        # Fallback in case message does not match any status code
        status_code = random.choice(list(http_status_codes.keys()))
        return f"{timestamp} {log_level} HTTP/1.1 {status_code} {message}"
    else:
        return f"{timestamp} {log_level} {message}"

def write_logs(rate, duration, log_file=None, http_format_logs=http_format_logs, custom_app_names=custom_app_names):
    """Write logs at a specified rate for a given duration."""
    end_time = time.time() + duration
    bytes_per_second = int(rate * 1024 * 1024)
    lines_per_second = bytes_per_second // log_line_size

    while time.time() < end_time:
        start_time = time.time()
        for _ in range(int(lines_per_second)):
            log_line = generate_log_line(http_format_logs, custom_app_names)
            if log_file:
                log_file.write(f"{log_line}\n")
            else:
                print(log_line)
        elapsed_time = time.time() - start_time
        time_to_sleep = max(0, 1 - elapsed_time)
        time.sleep(time_to_sleep)

def write_logs_random_rate(duration, rate_min, rate_max, log_file=None, http_format_logs=http_format_logs, custom_app_names=custom_app_names):
    """Write logs at a random rate between rate_min and rate_max for a given duration."""
    end_time = time.time() + duration
    remaining_time = duration

    if random.random() < rate_change_probability:
        change_percentage = random.uniform(-rate_change_max_percentage, rate_change_max_percentage)
        rate_max *= (1 + change_percentage)
        print(f"Changing rate_max by {change_percentage*100:.2f}%, new rate_max: {rate_max:.2f} MB/s")

    while remaining_time > 0:
        segment_duration = random.uniform(1, remaining_time)
        rate = random.uniform(rate_min, rate_max)
        write_logs(rate, segment_duration, log_file, http_format_logs, custom_app_names)
        remaining_time -= segment_duration

def write_logs_random_segments(total_duration, segment_max_duration, rate_min, rate_max, base_exit_probability, log_file=None, http_format_logs=http_format_logs, custom_app_names=custom_app_names):
    """Write logs in random segments with a chance to exit early."""
    remaining_time = total_duration
    while remaining_time > 0:
        exit_probability = base_exit_probability * random.uniform(0.5, 1.5)  # Add variability to the exit probability
        if random.random() < exit_probability:
            print("Exiting early based on random exit clause.")
            return
        segment_duration = random.uniform(1, min(segment_max_duration, remaining_time))
        write_logs_random_rate(segment_duration, rate_min, rate_max, log_file, http_format_logs, custom_app_names)
        remaining_time -= segment_duration

def main(duration_normal, duration_peak, rate_normal_min, rate_normal_max, rate_peak, log_line_size, base_exit_probability, rate_change_probability, rate_change_max_percentage, write_to_file, log_file_path, http_format_logs, stop_after_seconds, custom_app_names):
    start_time = time.time()
    if write_to_file:
        with open(log_file_path, 'w') as log_file:
            while stop_after_seconds == -1 or time.time() - start_time < stop_after_seconds:
                # Normal logging period with random segments
                write_logs_random_segments(duration_normal, 5, rate_normal_min, rate_normal_max, base_exit_probability, log_file, http_format_logs, custom_app_names)  # segments up to 5 seconds

                # Peak logging period
                write_logs_random_rate(duration_peak, rate_normal_max, rate_peak, log_file, http_format_logs, custom_app_names)
    else:
        while stop_after_seconds == -1 or time.time() - start_time < stop_after_seconds:
            # Normal logging period with random segments
            write_logs_random_segments(duration_normal, 5, rate_normal_min, rate_normal_max, base_exit_probability, None, http_format_logs, custom_app_names)  # segments up to 5 seconds

            # Peak logging period
            write_logs_random_rate(duration_peak, rate_normal_max, rate_peak, None, http_format_logs, custom_app_names)

if __name__ == "__main__":
    main(duration_normal, duration_peak, rate_normal_min, rate_normal_max, rate_peak, log_line_size, base_exit_probability, rate_change_probability, rate_change_max_percentage, write_to_file, log_file_path, http_format_logs, stop_after_seconds, custom_app_names)

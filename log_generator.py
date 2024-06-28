import random
import time
import datetime
import ipaddress
import threading
import statistics
import logging
import signal
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default configuration values
CONFIG = {
    'duration_normal': 10,
    'duration_peak': 2,
    'rate_normal_min': 0.0001,
    'rate_normal_max': 0.5500,
    'rate_peak': 2.000,
    'log_line_size': 100,
    'base_exit_probability': 0.05,
    'rate_change_probability': 0.1,
    'rate_change_max_percentage': 0.1,
    'write_to_file': True,
    'log_file_path': 'logs2.txt',
    'http_format_logs': False,
    'stop_after_seconds': -1,
    'custom_app_names': [],
    'custom_log_format': "{timestamp}, {log_level}, {message}"
}

log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

http_status_codes = {
    '200 OK': [
        'API request received', 'API response sent', 'Application deployment completed', 'Application deployment started',
        'Application rollback completed', 'Application rollback initiated', 'Backup completed successfully', 'Cache cleared',
        'Configuration updated', 'Database connection established', 'Data fetched successfully', 'Data processed successfully',
        'Email sent successfully', 'File uploaded successfully', 'New user registered', 'Password change requested',
        'Password change successful', 'Payment transaction completed', 'Scheduled task completed', 'Scheduled task started',
        'Service health check passed', 'Service started', 'Service stopped', 'Session token refreshed', 'SMS sent successfully',
        'User account unlocked', 'User login successful', 'User logged out', 'User profile updated', 'System reboot initiated',
        'System reboot completed', 'Malware removal successful', 'Service restored', 'Application error report generated',
        'Bug report submitted', 'Feature request submitted', 'Feature request approved', 'System update available', 'System update completed',
        'Firmware upgrade initiated', 'Firmware upgrade completed', 'User subscription created', 'Trial period started',
        'Database migration started', 'Database migration completed', 'System performance optimized', 'Debugging session started',
        'Debugging session ended', 'File download started', 'File download completed', 'Cloud resource provisioned', 'API key generated',
        'System backup scheduled', 'Encryption key rotation started', 'Encryption key rotation completed', 'Security audit started',
        'Security audit completed', 'User role updated'
    ],
    '400 Bad Request': [
        'Invalid user input detected', 'Configuration validation error', 'Credit card validation error', 'License key expired',
        'Service rate limit exceeded', 'Service quota exceeded'
    ],
    '401 Unauthorized': [
        'User login failed', 'Permission denied', 'Unauthorized access attempt detected'
    ],
    '403 Forbidden': ['Permission denied'],
    '404 Not Found': ['File not found', 'Service endpoint deprecated', 'Service endpoint removed'],
    '500 Internal Server Error': [
        'Error fetching data from database', 'Unexpected error occurred', 'Resource allocation failure', 'Database connection lost',
        'Cache update failed', 'Backup failed', 'Password change failed', 'Service health check failed', 'File upload failed',
        'User profile update failed', 'Email delivery failed', 'SMS delivery failed', 'Payment transaction failed', 'User account locked',
        'Service degraded', 'High memory usage detected', 'Memory leak detected', 'System backup cancelled', 'User subscription cancelled',
        'Trial period ended', 'Database migration started', 'Database migration completed', 'Cloud resource deprovisioned', 'API key revoked',
        'User role update failed'
    ]
}

user_agent_browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
user_agent_systems = [
    "Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7", "iPhone; CPU iPhone OS 14_6 like Mac OS X",
    "X11; Linux x86_64", "Linux; Android 10", "iPad; CPU OS 14_6 like Mac OS X", "Macintosh; Intel Mac OS X 11_2_3"
]

def generate_random_user_agent():
    """Generate a completely random user agent."""
    browser = random.choice(user_agent_browsers)
    system = random.choice(user_agent_systems)
    version = {
        "Chrome": f"Chrome/{random.randint(70, 100)}.0.{random.randint(3000, 4000)}.124",
        "Firefox": f"Firefox/{random.randint(70, 100)}.0",
        "Safari": f"Safari/{random.randint(605, 610)}.1.15",
        "Edge": f"Edg/{random.randint(80, 100)}.0.{random.randint(800, 900)}.59",
        "Opera": f"Opera/{random.randint(60, 70)}.0.{random.randint(3000, 4000)}.80"
    }
    return f"Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) {version[browser]}"

class TokenBucket:
    def __init__(self, rate, capacity):
        """Initialize the TokenBucket with a given rate and capacity."""
        self.rate = rate  # tokens added per second
        self.capacity = capacity  # max tokens in the bucket
        self.tokens = capacity
        self.timestamp = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens):
        """Consume tokens from the bucket in a thread-safe manner."""
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.timestamp
            self.tokens += elapsed * self.rate
            if self.tokens > self.capacity:
                self.tokens = self.capacity
            self.timestamp = current_time

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class Metrics:
    def __init__(self):
        """Initialize the Metrics with default values."""
        self.total_logs = 0
        self.total_bytes = 0
        self.rates = []
        self.start_time = time.time()
        self.lock = threading.Lock()

    def update(self, logs, bytes):
        """Update the metrics with the given logs and bytes in a thread-safe manner."""
        with self.lock:
            self.total_logs += logs
            self.total_bytes += bytes
            duration = time.time() - self.start_time
            if duration > 0:
                self.rates.append(bytes / duration / 1024 / 1024)  # MB/s

    def get_stats(self):
        """Get the current statistics in a thread-safe manner."""
        with self.lock:
            duration = time.time() - self.start_time
            avg_rate = statistics.mean(self.rates) if self.rates else 0
            max_rate = max(self.rates) if self.rates else 0
            min_rate = min(self.rates) if self.rates else 0
        return {
            "total_logs": self.total_logs,
            "total_bytes": self.total_bytes,
            "duration": duration,
            "avg_rate_mb_s": avg_rate,
            "max_rate_mb_s": max_rate,
            "min_rate_mb_s": min_rate
        }

def generate_ip_address():
    """Generate a random IP address."""
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_log_line(http_format_logs=CONFIG['http_format_logs'], custom_app_names=CONFIG['custom_app_names'], custom_format=CONFIG['custom_log_format']):
    """Generate a single log line with a timestamp and realistic message."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_level = random.choice(log_levels)

    if http_format_logs:
        ip_address = generate_ip_address()
        user_agent = generate_random_user_agent()
        status_code = random.choice(list(http_status_codes.keys()))
        message = random.choice(http_status_codes[status_code])
        return f"{timestamp} {log_level} {ip_address} - \"{user_agent}\" HTTP/1.1 {status_code} {message}"
    else:
        message = random.choice([msg for messages in http_status_codes.values() for msg in messages])

        if custom_app_names:
            app_name = random.choice(custom_app_names)
            message = f"{app_name}: {message}"

        if not custom_format:
            return f"{timestamp}, {log_level}, {message}"

        try:
            return custom_format.format(
                timestamp=timestamp,
                log_level=log_level,
                message=message
            )
        except KeyError as e:
            logging.error(f"Missing key {e} in custom format. Using default format.")
            return f"{timestamp}, {log_level}, {message}"
        except Exception as e:
            logging.error(f"Error formatting log line: {e}. Using default format.")
            return f"{timestamp}, {log_level}, {message}"

def write_logs(rate, duration, log_file=None, http_format_logs=CONFIG['http_format_logs'], custom_app_names=CONFIG['custom_app_names'], custom_format=CONFIG['custom_log_format'], metrics=None):
    """Write logs at a specified rate for a given duration using the token bucket algorithm."""
    logging.info(f"Writing logs at rate: {rate:.4f} MB/s for {duration:.2f} seconds")
    token_bucket = TokenBucket(rate * 1024 * 1024 / CONFIG['log_line_size'], rate * 1024 * 1024 / CONFIG['log_line_size'])
    end_time = time.time() + duration
    logs_written = 0
    bytes_written = 0

    while time.time() < end_time:
        if token_bucket.consume(1):
            log_line = generate_log_line(http_format_logs, custom_app_names, custom_format)
            try:
                if log_file:
                    log_file.write(f"{log_line}\n")
                else:
                    print(log_line)
                logs_written += 1
                bytes_written += len(log_line) + 1  # +1 for newline
            except (IOError, OSError) as e:
                logging.error(f"Error writing log: {e}")
        else:
            time.sleep(0.01)  # Sleep for a short time if no tokens are available

    if metrics:
        metrics.update(logs_written, bytes_written)

def write_logs_random_rate(duration, rate_min, rate_max, log_file=None, http_format_logs=CONFIG['http_format_logs'], custom_app_names=CONFIG['custom_app_names'], custom_format=CONFIG['custom_log_format'], metrics=None):
    """Write logs at a random rate between rate_min and rate_max for a given duration using the token bucket algorithm."""
    end_time = time.time() + duration
    remaining_time = duration

    if random.random() < CONFIG['rate_change_probability']:
        change_percentage = random.uniform(-CONFIG['rate_change_max_percentage'], CONFIG['rate_change_max_percentage'])
        rate_max *= (1 + change_percentage)
        logging.info(f"Changing rate_max by {change_percentage*100:.2f}%, new rate_max: {rate_max:.4f} MB/s")

    while remaining_time > 0:
        segment_duration = random.uniform(1, remaining_time)
        rate = random.uniform(rate_min, rate_max)
        logging.info(f"Selected random rate: {rate:.4f} MB/s")
        write_logs(rate, segment_duration, log_file, http_format_logs, custom_app_names, custom_format, metrics)
        remaining_time -= segment_duration

def write_logs_random_segments(total_duration, segment_max_duration, rate_min, rate_max, base_exit_probability, log_file=None, http_format_logs=CONFIG['http_format_logs'], custom_app_names=CONFIG['custom_app_names'], custom_format=CONFIG['custom_log_format'], metrics=None):
    """Write logs in random segments with a chance to exit early using the token bucket algorithm."""
    remaining_time = total_duration
    while remaining_time > 0:
        exit_probability = base_exit_probability * random.uniform(0.5, 1.5)  # Add variability to the exit probability
        if random.random() < exit_probability:
            logging.info("Exiting early based on random exit clause.")
            return
        segment_duration = random.uniform(1, min(segment_max_duration, remaining_time))
        write_logs_random_rate(segment_duration, rate_min, rate_max, log_file, http_format_logs, custom_app_names, custom_format, metrics)
        remaining_time -= segment_duration

def main(config, metrics_instance=None):
    """Main function to initiate log writing based on configuration."""
    start_time = time.time()
    iteration = 0

    if metrics_instance is None:
        metrics_instance = Metrics()

    def handle_interrupt(signal, frame):
        """Handle interrupt signals to ensure proper cleanup."""
        logging.info("Interrupt received, shutting down...")
        print(f"Final metrics: {metrics_instance.get_stats()}")
        exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    if config['write_to_file']:
        try:
            with open(config['log_file_path'], 'w') as log_file:
                while config['stop_after_seconds'] == -1 or time.time() - start_time < config['stop_after_seconds']:
                    write_logs_random_segments(config['duration_normal'], 5, config['rate_normal_min'], config['rate_normal_max'], config['base_exit_probability'], log_file, config['http_format_logs'], config['custom_app_names'], config['custom_log_format'], metrics_instance)
                    write_logs_random_rate(config['duration_peak'], config['rate_normal_max'], config['rate_peak'], log_file, config['http_format_logs'], config['custom_app_names'], config['custom_log_format'], metrics_instance)

                    iteration += 1
                    logging.info(f"Iteration {iteration} metrics: {metrics_instance.get_stats()}")
        except (IOError, OSError) as e:
            logging.error(f"Error opening or writing to file: {e}")
        finally:
            logging.info(f"Final metrics: {metrics_instance.get_stats()}")
    else:
        try:
            while config['stop_after_seconds'] == -1 or time.time() - start_time < config['stop_after_seconds']:
                write_logs_random_segments(config['duration_normal'], 5, config['rate_normal_min'], config['rate_normal_max'], config['base_exit_probability'], None, config['http_format_logs'], config['custom_app_names'], config['custom_log_format'], metrics_instance)
                write_logs_random_rate(config['duration_peak'], config['rate_normal_max'], config['rate_peak'], None, config['http_format_logs'], config['custom_app_names'], config['custom_log_format'], metrics_instance)

                iteration += 1
                logging.info(f"Iteration {iteration} metrics: {metrics_instance.get_stats()}")
        except Exception as e:
            logging.error(f"An error occurred during log generation: {e}")
        finally:
            logging.info(f"Final metrics: {metrics_instance.get_stats()}")

if __name__ == "__main__":
    main(CONFIG)

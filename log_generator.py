import random
import time
import datetime
import ipaddress
import threading
import statistics
import logging
import signal
import os
import yaml
import string

# Load configuration from config.yaml
try:
    with open('config.yaml', 'r') as f:
        config_data = yaml.safe_load(f)
except FileNotFoundError:
    print("Configuration file 'config.yaml' not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error parsing 'config.yaml': {e}")
    exit(1)

# Extract configurations
CONFIG = config_data.get('CONFIG', {})
log_levels = config_data.get('log_levels', [])
http_status_codes = config_data.get('http_status_codes', {})
user_agent_browsers = config_data.get('user_agent_browsers', [])
user_agent_systems = config_data.get('user_agent_systems', [])

# Configure logging
logging_level = CONFIG.get('logging_level', 'INFO').upper()
logging.basicConfig(level=getattr(logging, logging_level, logging.INFO),
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure required configuration parameters are present
required_config_keys = [
    'duration_normal',
    'duration_peak',
    'rate_normal_min',
    'rate_normal_max',
    'rate_peak',
    'log_line_size',
    'base_exit_probability',
    'rate_change_probability',
    'rate_change_max_percentage',
    'write_to_file',
    'log_file_path',
    'log_rotation_enabled',
    'log_rotation_size',
    'http_format_logs',
    'stop_after_seconds',
    'custom_app_names',
    'custom_log_format'
]

for key in required_config_keys:
    if key not in CONFIG:
        logging.error(f"Missing configuration parameter: {key}")
        exit(1)

# Precompute messages and templates to avoid recomputing every time
if CONFIG['http_format_logs']:
    # For HTTP format logs, precompute status codes and their messages
    http_status_code_list = list(http_status_codes.keys())
    http_messages = http_status_codes  # Already a dictionary
else:
    # For custom format logs, create a single list of all messages
    all_messages = [msg for messages in http_status_codes.values() for msg in messages]
    # Precompile the custom log format template
    custom_log_template = string.Template(CONFIG['custom_log_format'])

# Create a pool of pre-generated user agents
def generate_random_user_agent_uncached():
    """Generate a random user agent without caching."""
    browser = random.choice(user_agent_browsers)
    system = random.choice(user_agent_systems)
    version = {
        "Chrome": f"Chrome/{random.randint(70, 100)}.0.{random.randint(3000, 4000)}.124",
        "Firefox": f"Firefox/{random.randint(70, 100)}.0",
        "Safari": f"Safari/{random.randint(605, 610)}.1.15",
        "Edge": f"Edg/{random.randint(80, 100)}.0.{random.randint(800, 900)}.59",
        "Opera": f"Opera/{random.randint(60, 70)}.0.{random.randint(3000, 4000)}.80"
    }
    user_agent = f"Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) {version[browser]}"
    return user_agent

user_agent_pool = [generate_random_user_agent_uncached() for _ in range(100)]

def generate_random_user_agent():
    """Select a random user agent from the pre-generated pool."""
    return random.choice(user_agent_pool)

def generate_ip_address():
    """Generate a random IP address."""
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_log_line(http_format_logs=CONFIG['http_format_logs'],
                      custom_app_names=CONFIG['custom_app_names']):
    """
    Generate a single log line with a timestamp and realistic message.

    Args:
        http_format_logs (bool): Whether to generate logs in HTTP format.
        custom_app_names (List[str]): List of custom application names to include in logs.

    Returns:
        str: A formatted log line.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_level = random.choice(log_levels)

    if http_format_logs:
        ip_address = generate_ip_address()
        user_agent = generate_random_user_agent()
        status_code = random.choice(http_status_code_list)
        message = random.choice(http_messages[status_code])
        return f"{timestamp} {log_level} {ip_address} - \"{user_agent}\" HTTP/1.1 {status_code} {message}"
    else:
        message = random.choice(all_messages)

        if custom_app_names:
            app_name = random.choice(custom_app_names)
            message = f"{app_name}: {message}"

        try:
            return custom_log_template.substitute(
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

    def format_stats(self):
        """Format the statistics into a human-readable string with rounded numbers."""
        stats = self.get_stats()
        total_mb = stats['total_bytes'] / (1024 * 1024)  # Convert bytes to MB
        formatted_stats = (
            f"Total Logs: {stats['total_logs']:,}, "
            f"Total Data: {total_mb:.3f} MB, "
            f"Duration: {stats['duration']:.3f} seconds, "
            f"Average Rate: {stats['avg_rate_mb_s']:.3f} MB/s, "
            f"Maximum Rate: {stats['max_rate_mb_s']:.3f} MB/s, "
            f"Minimum Rate: {stats['min_rate_mb_s']:.3f} MB/s"
        )
        return formatted_stats

def rotate_log_file(log_file_path):
    """Rotate the log file by renaming the current log file and creating a new one."""
    base, ext = os.path.splitext(log_file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rotated_log_file_path = f"{base}_{timestamp}{ext}"
    if os.path.exists(log_file_path):
        os.rename(log_file_path, rotated_log_file_path)
        logging.info(f"Rotated log file to: {rotated_log_file_path}")
    else:
        logging.warning(f"Log file {log_file_path} does not exist. Skipping rotation.")
    return open(log_file_path, 'w')

def write_logs(rate, duration, log_file=None,
               http_format_logs=CONFIG['http_format_logs'],
               custom_app_names=CONFIG['custom_app_names'],
               metrics=None):
    logging.info(f"Writing logs at rate: {rate:.4f} MB/s for {duration:.2f} seconds")
    tokens_per_second = rate * 1024 * 1024 / CONFIG['log_line_size']
    token_bucket = TokenBucket(tokens_per_second, tokens_per_second)
    end_time = time.time() + duration
    logs_written = 0
    bytes_written = 0

    # Initial batch size
    batch_size = 1024
    log_lines = []
    expected_batch_time = batch_size / tokens_per_second

    # Introduce a variable to track time spent sleeping
    total_sleep_time = 0

    while time.time() < end_time:
        start_time = time.time()

        # Ensure batch_size is an integer
        batch_size = int(batch_size)

        if token_bucket.consume(batch_size):  # Check if we can write `batch_size` logs
            for _ in range(batch_size):
                log_line = generate_log_line(http_format_logs, custom_app_names)
                log_lines.append(log_line)
                logs_written += 1
                bytes_written += len(log_line) + 1  # +1 for newline

            if log_file:
                if CONFIG['log_rotation_enabled'] and log_file.tell() >= CONFIG['log_rotation_size'] * 1024 * 1024:
                    log_file.close()
                    log_file = rotate_log_file(CONFIG['log_file_path'])
                log_file.write('\n'.join(log_lines) + '\n')
                log_file.flush()
            else:
                print('\n'.join(log_lines))

            log_lines.clear()

            # Calculate the time taken to process this batch
            elapsed_time = time.time() - start_time
            sleep_time = max(0, expected_batch_time - elapsed_time)

            # Aggressive batch size adjustment based on sleep time
            if sleep_time > 0:
                total_sleep_time += sleep_time
                # If we're spending too much time sleeping, increase the batch size
                # Increase batch size by 20% if sleep time is significant
                if total_sleep_time > 0.05:  # Adjust this threshold as needed
                    batch_size = min(batch_size * 1.2, tokens_per_second)  # Ensure we don’t exceed the rate
                    total_sleep_time = 0  # Reset the sleep tracker
                    logging.info(f"Increasing batch size to: {int(batch_size)}")
            else:
                # If not sleeping, increase batch size more aggressively
                batch_size = min(batch_size * 1.5, tokens_per_second)
                logging.info(f"Rapidly increasing batch size to: {int(batch_size)}")

            # Sleep if necessary
            time.sleep(sleep_time)

        else:
            time.sleep(0.05)  # Sleep for a short time if no tokens are available

    if metrics:
        metrics.update(logs_written, bytes_written)

    return log_file

def write_logs_random_rate(duration, rate_min, rate_max, log_file=None,
                           http_format_logs=CONFIG['http_format_logs'],
                           custom_app_names=CONFIG['custom_app_names'],
                           metrics=None):
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
        log_file = write_logs(rate, segment_duration, log_file, http_format_logs, custom_app_names, metrics)
        remaining_time -= segment_duration

    return log_file

def write_logs_random_segments(total_duration, segment_max_duration, rate_min, rate_max,
                               base_exit_probability, log_file=None,
                               http_format_logs=CONFIG['http_format_logs'],
                               custom_app_names=CONFIG['custom_app_names'],
                               metrics=None):
    """Write logs in random segments with a chance to exit early using the token bucket algorithm."""
    remaining_time = total_duration
    while remaining_time > 0:
        exit_probability = base_exit_probability * random.uniform(0.5, 1.5)  # Add variability to the exit probability
        if random.random() < exit_probability:
            logging.info("Exiting early based on random exit clause.")
            return log_file
        segment_duration = random.uniform(1, min(segment_max_duration, remaining_time))
        log_file = write_logs_random_rate(segment_duration, rate_min, rate_max, log_file,
                                          http_format_logs, custom_app_names, metrics)
        remaining_time -= segment_duration

    return log_file

def main(config, metrics_instance=None):
    """Main function to initiate log writing based on configuration."""
    start_time = time.time()
    iteration = 0

    if metrics_instance is None:
        metrics_instance = Metrics()

    interrupted = False  # Flag to indicate if an interrupt was received

    def handle_interrupt(signal_received, frame):
        """Handle interrupt signals to ensure proper cleanup."""
        nonlocal interrupted
        interrupted = True
        logging.info("Interrupt received, shutting down...")
        logging.info(f"Final metrics: {metrics_instance.format_stats()}")
        exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    if config['write_to_file']:
        try:
            with open(config['log_file_path'], 'a') as log_file:
                while config['stop_after_seconds'] == -1 or time.time() - start_time < config['stop_after_seconds']:
                    log_file = write_logs_random_segments(
                        config['duration_normal'],
                        5,
                        config['rate_normal_min'],
                        config['rate_normal_max'],
                        config['base_exit_probability'],
                        log_file,
                        config['http_format_logs'],
                        config['custom_app_names'],
                        metrics_instance
                    )
                    log_file = write_logs_random_rate(
                        config['duration_peak'],
                        config['rate_normal_max'],
                        config['rate_peak'],
                        log_file,
                        config['http_format_logs'],
                        config['custom_app_names'],
                        metrics_instance
                    )

                    iteration += 1
                    logging.info(f"Iteration {iteration} metrics: {metrics_instance.format_stats()}")
        except (IOError, OSError) as e:
            logging.error(f"Error opening or writing to file: {e}")
        finally:
            if not interrupted:
                logging.info(f"Final metrics: {metrics_instance.format_stats()}")
    else:
        try:
            while config['stop_after_seconds'] == -1 or time.time() - start_time < config['stop_after_seconds']:
                write_logs_random_segments(
                    config['duration_normal'],
                    5,
                    config['rate_normal_min'],
                    config['rate_normal_max'],
                    config['base_exit_probability'],
                    None,
                    config['http_format_logs'],
                    config['custom_app_names'],
                    metrics_instance
                )
                write_logs_random_rate(
                    config['duration_peak'],
                    config['rate_normal_max'],
                    config['rate_peak'],
                    None,
                    config['http_format_logs'],
                    config['custom_app_names'],
                    metrics_instance
                )

                iteration += 1
                logging.info(f"Iteration {iteration} metrics: {metrics_instance.format_stats()}")
        except Exception as e:
            logging.error(f"An error occurred during log generation: {e}")
        finally:
            if not interrupted:
                logging.info(f"Final metrics: {metrics_instance.format_stats()}")

if __name__ == "__main__":
    main(CONFIG)

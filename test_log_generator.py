import pytest
from log_generator import (
    generate_log_line,
    write_logs,
    write_logs_random_rate,
    write_logs_random_segments
)

# Override the configurations for testing
duration_normal = 2  # seconds
duration_peak = 1  # seconds
rate_normal_min = 0.0001  # MB/s
rate_normal_max = 0.001  # MB/s
rate_peak = 0.002  # MB/s
log_line_size = 50  # Average size of a log line in bytes
base_exit_probability = 0.1  # Base 10% chance to exit early
rate_change_probability = 0.2  # 20% chance to change rate_max
rate_change_max_percentage = 0.1  # Maximum 10% change in rate_max
stop_after_seconds = 10  # Stop the script after 2 seconds for testing

def test_generate_log_line():
    log_line = generate_log_line()
    assert log_line is not None
    assert len(log_line) > 0

def test_write_logs(tmp_path):
    log_file_path = tmp_path / "test_logs.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs(rate_normal_min, duration_normal, log_file)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_rate(tmp_path):
    log_file_path = tmp_path / "test_logs_random_rate.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_rate(duration_peak, rate_normal_min, rate_normal_max, log_file)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_segments(tmp_path):
    log_file_path = tmp_path / "test_logs_random_segments.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_segments(duration_normal, 1, rate_normal_min, rate_normal_max, base_exit_probability, log_file)
    assert log_file_path.read_text().strip() != ""

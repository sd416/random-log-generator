import pytest
import time
from log_generator import (
    generate_log_line,
    write_logs,
    write_logs_random_rate,
    write_logs_random_segments,
    main
)
# Override the configurations for testing
test_duration_normal = 2  # seconds
test_duration_peak = 1  # seconds
test_rate_normal_min = 0.0001  # MB/s
test_rate_normal_max = 0.001  # MB/s
test_rate_peak = 0.002  # MB/s
test_log_line_size = 50  # Average size of a log line in bytes
test_base_exit_probability = 0.1  # Base 10% chance to exit early
test_rate_change_probability = 0.2  # 20% chance to change rate_max
test_rate_change_max_percentage = 0.1  # Maximum 10% change in rate_max
test_stop_after_seconds = 2  # Stop the script after 2 seconds for testing

def test_generate_log_line():
    print("Testing generate_log_line")
    log_line = generate_log_line(http_format_logs=False)
    assert log_line is not None
    assert len(log_line) > 0

def test_write_logs(tmp_path):
    print("Testing write_logs")
    log_file_path = tmp_path / "test_logs.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs(test_rate_normal_min, test_duration_normal, log_file, http_format_logs=False)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_rate(tmp_path):
    print("Testing write_logs_random_rate")
    log_file_path = tmp_path / "test_logs_random_rate.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_rate(test_duration_peak, test_rate_normal_min, test_rate_normal_max, log_file, http_format_logs=False)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_segments(tmp_path):
    print("Testing write_logs_random_segments")
    log_file_path = tmp_path / "test_logs_random_segments.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_segments(test_duration_normal, 1, test_rate_normal_min, test_rate_normal_max, test_base_exit_probability, log_file, http_format_logs=False)
    assert log_file_path.read_text().strip() != ""

def test_main(tmp_path):
    print("Testing main function")
    log_file_path = tmp_path / "test_main_logs.txt"
    start_time = time.time()
    timeout = 10  # seconds
    while time.time() - start_time < timeout:
        main(test_duration_normal, test_duration_peak, test_rate_normal_min, test_rate_normal_max, test_rate_peak, test_log_line_size, test_base_exit_probability, test_rate_change_probability, test_rate_change_max_percentage, True, str(log_file_path), False, test_stop_after_seconds)
        if log_file_path.read_text().strip() != "":
            break
    assert log_file_path.read_text().strip() != ""

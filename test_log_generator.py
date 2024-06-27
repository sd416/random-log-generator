import pytest
import time
from log_generator import generate_log_line, write_logs, write_logs_random_rate, write_logs_random_segments, main, generate_random_user_agent, generate_ip_address

# Override the configurations for testing
test_config = {
    'duration_normal': 5,
    'duration_peak': 2,
    'rate_normal_min': 0.0001,
    'rate_normal_max': 0.001,
    'rate_peak': 0.002,
    'log_line_size': 50,
    'base_exit_probability': 0.1,
    'rate_change_probability': 0.2,
    'rate_change_max_percentage': 0.1,
    'write_to_file': True,
    'log_file_path': 'logs.txt',
    'http_format_logs': False,
    'stop_after_seconds': 21,
    'custom_app_names': ['App1', 'App2', 'App3'],
    'custom_log_format': "{timestamp} {log_level} {ip_address} {user_agent} {message}"
}

def test_generate_log_line():
    print("Testing generate_log_line")
    log_line = generate_log_line(http_format_logs=test_config['http_format_logs'], custom_app_names=test_config['custom_app_names'])
    assert log_line is not None
    assert len(log_line) > 0

def test_generate_random_user_agent():
    print("Testing generate_random_user_agent")
    user_agent = generate_random_user_agent()
    assert user_agent is not None
    assert "Mozilla/5.0" in user_agent

def test_generate_ip_address():
    print("Testing generate_ip_address")
    ip_address = generate_ip_address()
    assert ip_address is not None
    assert ipaddress.ip_address(ip_address)

def test_write_logs(tmp_path):
    print("Testing write_logs")
    log_file_path = tmp_path / "test_logs.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs(test_config['rate_normal_min'], test_config['duration_normal'], log_file, http_format_logs=test_config['http_format_logs'], custom_app_names=test_config['custom_app_names'])
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_rate(tmp_path):
    print("Testing write_logs_random_rate")
    log_file_path = tmp_path / "test_logs_random_rate.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_rate(test_config['duration_peak'], test_config['rate_normal_min'], test_config['rate_normal_max'], log_file, http_format_logs=test_config['http_format_logs'], custom_app_names=test_config['custom_app_names'])
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_segments(tmp_path):
    print("Testing write_logs_random_segments")
    log_file_path = tmp_path / "test_logs_random_segments.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_segments(test_config['duration_normal'], 1, test_config['rate_normal_min'], test_config['rate_normal_max'], test_config['base_exit_probability'], log_file, http_format_logs=test_config['http_format_logs'], custom_app_names=test_config['custom_app_names'])
    assert log_file_path.read_text().strip() != ""

def test_main(tmp_path):
    print("Testing main function")
    log_file_path = tmp_path / "test_main_logs.txt"
    test_config['log_file_path'] = str(log_file_path)
    test_config['write_to_file'] = True
    test_config['stop_after_seconds'] = 21  # Ensure this matches the test configuration

    start_time = time.time()
    timeout = 10  # seconds
    while time.time() - start_time < timeout:
        main(test_config)
        if log_file_path.read_text().strip() != "":
            break
    assert log_file_path.read_text().strip() != ""

def test_main_no_file():
    print("Testing main function without file writing")
    test_config['write_to_file'] = False
    test_config['stop_after_seconds'] = 5  # Run for a shorter duration for testing
    main(test_config)
    assert metrics.get_stats()['total_logs'] > 0

def test_exit_early(tmp_path):
    print("Testing early exit in write_logs_random_segments")
    log_file_path = tmp_path / "test_exit_early.txt"
    test_config['base_exit_probability'] = 1.0  # Ensure early exit
    with open(log_file_path, 'w') as log_file:
        write_logs_random_segments(test_config['duration_normal'], 1, test_config['rate_normal_min'], test_config['rate_normal_max'], test_config['base_exit_probability'], log_file, test_config['http_format_logs'], test_config['custom_app_names'])
    assert log_file_path.read_text().strip() == ""

import time
import ipaddress
import random
import tempfile
import os
from log_generator import (
    generate_log_line, write_logs, write_logs_random_rate,
    write_logs_random_segments, main, generate_random_user_agent,
    generate_ip_address, Metrics, CONFIG
)

# Test configuration
test_config = {
    'duration_normal': 5,
    'duration_peak': 2,
    'rate_normal_min': 0.1,     # Increased rates
    'rate_normal_max': 0.5,
    'rate_peak': 1.0,
    'log_line_size': 100,
    'base_exit_probability': 0.1,
    'rate_change_probability': 0.2,
    'rate_change_max_percentage': 0.1,
    'write_to_file': True,
    'log_file_path': 'test_logs.txt',
    'log_rotation_enabled': False,
    'log_rotation_size': 1,
    'http_format_logs': False,
    'stop_after_seconds': 10,
    'custom_app_names': ['TestApp1', 'TestApp2'],
    'custom_log_format': "${timestamp} ${log_level} ${message}"
}

def test_generate_log_line():
    log_line = generate_log_line(
        http_format_logs=test_config['http_format_logs'],
        custom_app_names=test_config['custom_app_names'],
        custom_log_format=test_config['custom_log_format']
    )
    assert isinstance(log_line, str)
    assert len(log_line) > 0
    print(f"Generated log line: {log_line}")

def test_generate_random_user_agent():
    user_agent = generate_random_user_agent()
    assert isinstance(user_agent, str)
    assert "Mozilla/5.0" in user_agent
    print(f"Generated user agent: {user_agent}")

def test_generate_ip_address():
    ip_address = generate_ip_address()
    assert isinstance(ip_address, str)
    assert ipaddress.ip_address(ip_address)
    print(f"Generated IP address: {ip_address}")

def test_write_logs():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file_path = os.path.join(tmp_dir, "test_logs.txt")
        metrics_instance = Metrics()
        with open(log_file_path, 'w') as log_file:
            write_logs(
                test_config['rate_normal_min'], test_config['duration_normal'],
                log_file, http_format_logs=test_config['http_format_logs'],
                custom_app_names=test_config['custom_app_names'],
                custom_log_format=test_config['custom_log_format'],
                metrics=metrics_instance
            )
        assert os.path.getsize(log_file_path) > 0
        print(f"Logs written to {log_file_path}")

def test_write_logs_random_rate():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file_path = os.path.join(tmp_dir, "test_logs_random_rate.txt")
        metrics_instance = Metrics()
        with open(log_file_path, 'w') as log_file:
            write_logs_random_rate(
                test_config['duration_peak'], test_config['rate_normal_min'],
                test_config['rate_normal_max'], log_file, http_format_logs=test_config['http_format_logs'],
                custom_app_names=test_config['custom_app_names'],
                custom_log_format=test_config['custom_log_format'],
                metrics=metrics_instance
            )
        assert os.path.getsize(log_file_path) > 0
        print(f"Random rate logs written to {log_file_path}")

def test_write_logs_random_segments():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file_path = os.path.join(tmp_dir, "test_logs_random_segments.txt")
        metrics_instance = Metrics()
        with open(log_file_path, 'w') as log_file:
            write_logs_random_segments(
                test_config['duration_normal'], 1, test_config['rate_normal_min'],
                test_config['rate_normal_max'], test_config['base_exit_probability'],
                log_file, http_format_logs=test_config['http_format_logs'],
                custom_app_names=test_config['custom_app_names'],
                custom_log_format=test_config['custom_log_format'],
                metrics=metrics_instance
            )
        assert os.path.getsize(log_file_path) > 0
        print(f"Random segment logs written to {log_file_path}")

def test_main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file_path = os.path.join(tmp_dir, "test_main_logs.txt")
        test_config['log_file_path'] = log_file_path
        test_config['write_to_file'] = True
        test_config['stop_after_seconds'] = 5  # Reduced for faster testing

        main(test_config)
        assert os.path.getsize(log_file_path) > 0
        print(f"Main function logs written to {log_file_path}")

def test_main_no_file():
    test_config['write_to_file'] = False
    test_config['stop_after_seconds'] = 5  # Reduced for faster testing
    test_metrics = Metrics()

    main(test_config, metrics_instance=test_metrics)
    stats = test_metrics.get_stats()
    assert stats['total_logs'] > 0
    print(f"Main function without file writing generated {stats['total_logs']} logs")

def test_exit_early():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file_path = os.path.join(tmp_dir, "test_exit_early.txt")
        test_config['base_exit_probability'] = 1.0  # Ensure early exit
        metrics_instance = Metrics()
        with open(log_file_path, 'w') as log_file:
            write_logs_random_segments(
                test_config['duration_normal'], 1, test_config['rate_normal_min'],
                test_config['rate_normal_max'], test_config['base_exit_probability'],
                log_file, test_config['http_format_logs'], test_config['custom_app_names'],
                test_config['custom_log_format'],
                metrics=metrics_instance
            )
        assert os.path.getsize(log_file_path) == 0
        print("Early exit test passed")

if __name__ == "__main__":
    # Run all tests
    test_generate_log_line()
    test_generate_random_user_agent()
    test_generate_ip_address()
    test_write_logs()
    test_write_logs_random_rate()
    test_write_logs_random_segments()
    test_main()
    test_main_no_file()
    test_exit_early()
    print("All tests completed successfully")

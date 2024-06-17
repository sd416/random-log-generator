import pytest
from log_generator import generate_log_line, write_logs, write_logs_random_rate, write_logs_random_segments

def test_generate_log_line():
    log_line = generate_log_line()
    assert log_line is not None
    assert len(log_line) > 0

def test_write_logs(tmp_path):
    log_file_path = tmp_path / "test_logs.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs(0.001, 1, log_file)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_rate(tmp_path):
    log_file_path = tmp_path / "test_logs_random_rate.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_rate(1, 0.0001, 0.001, log_file)
    assert log_file_path.read_text().strip() != ""

def test_write_logs_random_segments(tmp_path):
    log_file_path = tmp_path / "test_logs_random_segments.txt"
    with open(log_file_path, 'w') as log_file:
        write_logs_random_segments(1, 5, 0.0001, 0.001, 0.1, log_file)
    assert log_file_path.read_text().strip() != ""

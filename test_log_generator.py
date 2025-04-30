import time
import ipaddress
import random
import tempfile
import os
import datetime
import unittest
from unittest import mock

# Import from the new package structure
from random_log_generator.core.generator import generate_log_line, write_logs, main
from random_log_generator.core.strategies import write_logs_random_rate, write_logs_random_segments
from random_log_generator.utils.ip_generator import generate_ip_address
from random_log_generator.utils.user_agents import generate_random_user_agent, initialize_user_agents, initialize_user_agent_pool
from random_log_generator.metrics.collector import Metrics
from random_log_generator.formatters.http import HTTPFormatter
from random_log_generator.formatters.custom import CustomFormatter
from random_log_generator.output.file_output import FileOutputHandler
from random_log_generator.output.console_output import ConsoleOutputHandler
from random_log_generator.core.rate_limiter import TokenBucket

# Test configuration
test_config = {
    'duration_normal': 5,
    'duration_peak': 2,
    'rate_normal_min': 0.1,     # Increased rates to ensure logs are written
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
    'http_format_logs': True,    # Set to True to match default CONFIG
    'stop_after_seconds': 10,
    'custom_app_names': ['TestApp1', 'TestApp2'],
    'custom_log_format': "${timestamp} ${log_level} ${message}"
}

# Mock HTTP status codes and log levels for testing
mock_http_status_codes = {
    "200": "OK",
    "404": "Not Found",
    "500": "Internal Server Error"
}

mock_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]


class TestLogGenerator(unittest.TestCase):
    """Test cases for the Random Log Generator."""
    
    def setUp(self):
        """Set up test environment."""
        # Initialize user agents
        initialize_user_agents(
            ["Chrome", "Firefox", "Safari"],
            ["Windows NT 10.0", "Macintosh; Intel Mac OS X 10_15_7"]
        )
        initialize_user_agent_pool(10)
        
        # Initialize formatters
        self.http_formatter = HTTPFormatter(mock_http_status_codes)
        self.custom_formatter = CustomFormatter(
            test_config['custom_log_format'],
            test_config['custom_app_names']
        )
    
    def test_generate_log_line(self):
        """Test generating a log line."""
        # Test with HTTP formatter
        log_line = generate_log_line(self.http_formatter, mock_log_levels)
        self.assertIsInstance(log_line, str)
        self.assertGreater(len(log_line), 0)
        print(f"Generated HTTP log line: {log_line}")
        
        # For custom formatter, we need to modify the generate_log_line function locally
        # since it requires a message parameter
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_level = random.choice(mock_log_levels)
        log_line = self.custom_formatter.format_log(timestamp, log_level, "Test message")
        self.assertIsInstance(log_line, str)
        self.assertGreater(len(log_line), 0)
        print(f"Generated custom log line: {log_line}")
    
    def test_generate_random_user_agent(self):
        """Test generating a random user agent."""
        user_agent = generate_random_user_agent()
        self.assertIsInstance(user_agent, str)
        self.assertIn("Mozilla/5.0", user_agent)
        print(f"Generated user agent: {user_agent}")
    
    def test_generate_ip_address(self):
        """Test generating a random IP address."""
        ip_address = generate_ip_address()
        self.assertIsInstance(ip_address, str)
        self.assertTrue(ipaddress.ip_address(ip_address))
        print(f"Generated IP address: {ip_address}")
    
    def test_write_logs(self):
        """Test writing logs at a constant rate."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file_path = os.path.join(tmp_dir, "test_logs.txt")
            metrics_instance = Metrics()
            
            # Create a file output handler
            output_handler = FileOutputHandler(log_file_path, False, 0)
            
            # Write logs
            success = write_logs(
                test_config['rate_normal_min'], 
                test_config['duration_normal'],
                output_handler,
                self.http_formatter,
                mock_log_levels,
                metrics_instance
            )
            
            # Close the output handler
            output_handler.close()
            
            # Check results
            self.assertTrue(success)
            self.assertGreater(os.path.getsize(log_file_path), 0)
            print(f"Logs written to {log_file_path}")
    
    def test_write_logs_random_rate(self):
        """Test writing logs at a random rate."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file_path = os.path.join(tmp_dir, "test_logs_random_rate.txt")
            metrics_instance = Metrics()
            
            # Create a file output handler
            output_handler = FileOutputHandler(log_file_path, False, 0)
            
            # Write logs with random rate
            success = write_logs_random_rate(
                test_config['duration_peak'],
                test_config['rate_normal_min'],
                test_config['rate_normal_max'],
                output_handler,
                self.http_formatter,
                mock_log_levels,
                metrics_instance
            )
            
            # Close the output handler
            output_handler.close()
            
            # Check results
            self.assertTrue(success)
            self.assertGreater(os.path.getsize(log_file_path), 0)
            print(f"Random rate logs written to {log_file_path}")
    
    def test_write_logs_random_segments(self):
        """Test writing logs in random segments."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file_path = os.path.join(tmp_dir, "test_logs_random_segments.txt")
            metrics_instance = Metrics()
            
            # Create a file output handler
            output_handler = FileOutputHandler(log_file_path, False, 0)
            
            # Use a very low exit probability to ensure logs are written
            # This helps prevent issues with different random number generation in Python 3.13
            very_low_exit_probability = 0.001
            
            # Write logs with random segments - use longer duration and higher rates
            success = write_logs_random_segments(
                10,  # Longer duration
                1,
                0.5,  # Higher minimum rate
                1.0,  # Higher maximum rate
                very_low_exit_probability,  # Much lower exit probability
                output_handler,
                self.http_formatter,
                mock_log_levels,
                metrics_instance
            )
            
            # Close the output handler
            output_handler.close()
            
            # Check results
            self.assertTrue(success)
            
            # Check if file exists and has content
            self.assertTrue(os.path.exists(log_file_path), "Log file was not created")
            file_size = os.path.getsize(log_file_path)
            self.assertGreater(file_size, 0, f"Log file is empty (size: {file_size})")
            print(f"Random segment logs written to {log_file_path} (size: {file_size} bytes)")
    
    def test_exit_early(self):
        """Test early exit from random segments."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file_path = os.path.join(tmp_dir, "test_exit_early.txt")
            metrics_instance = Metrics()
            
            # Create a file output handler
            output_handler = FileOutputHandler(log_file_path, False, 0)
            
            # Mock random.random to always return 0, which is less than base_exit_probability
            with mock.patch('random.random', return_value=0):
                success = write_logs_random_segments(
                    test_config['duration_normal'],
                    1,
                    test_config['rate_normal_min'],
                    test_config['rate_normal_max'],
                    1.0,  # Set base_exit_probability to 1.0 to ensure early exit
                    output_handler,
                    self.http_formatter,
                    mock_log_levels,
                    metrics_instance
                )
            
            # Close the output handler
            output_handler.close()
            
            # Check results
            self.assertTrue(success)
            self.assertEqual(os.path.getsize(log_file_path), 0)
            print("Early exit test passed")
    
    def test_main_with_file(self):
        """Test the main function with file output."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file_path = os.path.join(tmp_dir, "test_main_logs.txt")
            
            # Create a copy of the test config with updated file path
            config = test_config.copy()
            config['log_file_path'] = log_file_path
            config['write_to_file'] = True
            config['stop_after_seconds'] = 2  # Reduced for faster testing
            
            # Mock the config_loader.load_config function to return our test config
            with mock.patch('random_log_generator.config.config_loader.load_config', return_value=config):
                # Run the main function
                exit_code = main(config)
                
                # Check results
                self.assertEqual(exit_code, 0)
                self.assertGreater(os.path.getsize(log_file_path), 0)
                print(f"Main function logs written to {log_file_path}")
    
    def test_main_console_output(self):
        """Test the main function with console output."""
        # Create a copy of the test config
        config = test_config.copy()
        config['write_to_file'] = False
        config['stop_after_seconds'] = 2  # Reduced for faster testing
        
        # Create a metrics instance
        metrics_instance = Metrics()
        
        # Mock the config_loader.load_config function to return our test config
        with mock.patch('random_log_generator.config.config_loader.load_config', return_value=config):
            # Run the main function
            exit_code = main(config, metrics_instance)
            
            # Check results
            self.assertEqual(exit_code, 0)
            stats = metrics_instance.get_stats()
            self.assertGreater(stats['total_logs'], 0)
            print(f"Main function without file writing generated {stats['total_logs']} logs")
    
    # Additional unit tests for individual components
    
    def test_token_bucket(self):
        """Test the TokenBucket rate limiter."""
        # Create a token bucket with 10 tokens per second and a capacity of 10
        token_bucket = TokenBucket(10, 10)
        
        # Should be able to consume 10 tokens immediately
        self.assertTrue(token_bucket.consume(10))
        
        # Should not be able to consume any more tokens immediately
        self.assertFalse(token_bucket.consume(1))
        
        # Wait for 0.5 seconds, should be able to consume 5 tokens
        time.sleep(0.5)
        self.assertTrue(token_bucket.consume(5))
        self.assertFalse(token_bucket.consume(1))
        
        print("TokenBucket tests passed")
    
    def test_metrics_collector(self):
        """Test the Metrics collector."""
        metrics = Metrics()
        
        # Update metrics
        metrics.update(100, 1024)
        
        # Get stats
        stats = metrics.get_stats()
        
        # Check results
        self.assertEqual(stats['total_logs'], 100)
        self.assertEqual(stats['total_bytes'], 1024)
        self.assertGreater(stats['duration'], 0)
        self.assertGreater(stats['avg_rate_mb_s'], 0)
        
        print("Metrics collector tests passed")
    
    def test_http_formatter(self):
        """Test the HTTP formatter."""
        formatter = HTTPFormatter(mock_http_status_codes)
        
        # Format a log line
        timestamp = "2023-01-01T12:00:00Z"
        log_level = "INFO"
        log_line = formatter.format_log(timestamp, log_level)
        
        # Check results
        self.assertIsInstance(log_line, str)
        self.assertIn(timestamp, log_line)
        self.assertIn("HTTP", log_line)
        
        print(f"HTTP formatter test passed: {log_line}")
    
    def test_custom_formatter(self):
        """Test the custom formatter."""
        formatter = CustomFormatter(
            "${timestamp} ${log_level} [${app_name}] ${message}",
            ["TestApp"]
        )
        
        # Format a log line
        timestamp = "2023-01-01T12:00:00Z"
        log_level = "INFO"
        message = "This is a test message"
        log_line = formatter.format_log(timestamp, log_level, message)
        
        # Check results
        self.assertIsInstance(log_line, str)
        self.assertIn(timestamp, log_line)
        self.assertIn(log_level, log_line)
        self.assertIn("TestApp", log_line)
        self.assertIn(message, log_line)
        
        print(f"Custom formatter test passed: {log_line}")
    
    def test_console_output_handler(self):
        """Test the console output handler."""
        # Create a console output handler
        output_handler = ConsoleOutputHandler()
        
        # Write some log lines
        success = output_handler.write(["Test log line 1", "Test log line 2"])
        
        # Check results
        self.assertTrue(success)
        
        # Close the output handler
        output_handler.close()
        
        print("Console output handler test passed")


if __name__ == "__main__":
    unittest.main()

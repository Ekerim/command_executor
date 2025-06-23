import unittest
import logging
import sys
import os
from contextlib import redirect_stderr
from command_executor.main import run_cmd, _check_cached_connection, _cache_connection, _close_connections
from fabric import Connection

# Create a logger for your application
logger = logging.getLogger("command_executor")
logger.setLevel(logging.DEBUG)  # Set your desired logging level

# Create a custom filter to allow only logs from the local application
class LocalAppFilter(logging.Filter):
    def filter(self, record):
        return "command_executor" in record.name

# Add the filter to the logger
handler = logging.StreamHandler()  # You can use other handlers if needed
handler.setLevel(logging.DEBUG)  # Set the handler's logging level
handler.addFilter(LocalAppFilter())  # Add the custom filter
logger.addHandler(handler)

class TestCommandExecutor(unittest.TestCase):
    def setUp(self):
        # Ensure connections are cleared before each test
        _close_connections()

    def tearDown(self):
        # Ensure connections are cleared after each test
        _close_connections()

    def test_run_cmd_local(self):
        # Test a simple local command
        stdout, stderr, exit_code = run_cmd("echo 'Hello, Local!'")

        # Assertions
        self.assertEqual(stdout.strip(), "Hello, Local!")
        self.assertEqual(stderr, "")
        self.assertEqual(exit_code, 0)

    def test_check_cached_connection_none(self):
        # Test checking a non-existent cached connection
        connection = _check_cached_connection("localhost")
        self.assertIsNone(connection)

    def test_cache_connection_creation(self):
        # Test creating and caching a connection
        connection = _cache_connection("localhost", Connection(host="localhost"))
        self.assertIsInstance(connection, Connection)

        # Verify that the cached connection is returned
        cached_connection = _check_cached_connection("localhost")
        self.assertEqual(connection, cached_connection)

    def test_run_cmd_remote_single_host(self):
        # Test run_cmd with one remote host and parallel=False
        with redirect_stderr(open(os.devnull, 'w')):
            stdout, stderr, exit_code = run_cmd("echo 'Hello singular world'", hosts=["localhost"], parallel=False)

        # Assertions
        self.assertEqual(stdout.strip(), "Hello singular world")
        self.assertEqual(stderr, "")
        self.assertEqual(exit_code, 0)

    def test_run_cmd_remote_multiple_hosts_parallel(self):
        # Test run_cmd with multiple remote hosts and parallel=True
        with redirect_stderr(open(os.devnull, 'w')):
            stdout, stderr, exit_code = run_cmd("echo 'Hello parallel world'", hosts=["localhost"], parallel=True)

        # Assertions
        self.assertEqual(stdout, "Hello parallel world")
        self.assertEqual(stderr, "")
        self.assertEqual(exit_code, 0)

    def test_close_connections(self):
        # Test closing all cached connections
        _cache_connection("localhost", Connection(host="localhost"))
        _cache_connection("localhost2", Connection(host="localhost"))

        # Close all connections
        _close_connections()

        # Verify that all connections are cleared
        self.assertIsNone(_check_cached_connection("localhost"))
        self.assertIsNone(_check_cached_connection("localhost2"))


if __name__ == "__main__":
    unittest.main()
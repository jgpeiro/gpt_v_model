# unit_tests.py TEMPLATE
# This is a simplified example of unit tests for the Serial Terminal Application. 
# It demonstrates basic testing of the list_com_ports function and the SerialThread class.

import unittest
from unittest.mock import patch, MagicMock
from main import list_com_ports, SerialThread

class TestListComPorts(unittest.TestCase):
    """Test the list_com_ports function."""

    @patch('main.serial.tools.list_ports.comports')
    def test_list_com_ports(self, mock_comports):
        """Test that available COM ports are correctly listed."""
        # Setup mock
        mock_port1 = MagicMock(device='COM1')
        mock_port2 = MagicMock(device='COM2')
        mock_comports.return_value = [mock_port1, mock_port2]

        # Execute function
        ports = list_com_ports()

        # Verify
        self.assertEqual(ports, ['COM1', 'COM2'])

class TestSerialThread(unittest.TestCase):
    """Test the SerialThread class."""

    @patch('main.serial.Serial')
    def test_serial_thread_run_stop(self, mock_serial):
        """Test running and stopping the SerialThread."""
        # Setup mock
        mock_serial_instance = MagicMock()
        mock_serial.return_value = mock_serial_instance
        mock_serial_instance.readline.return_value = b'test data\n'

        # Initialize SerialThread
        serial_thread = SerialThread('COM1', 9600)

        # Start the thread
        serial_thread.start()

        # Simulate receiving data
        serial_thread.received.connect(self.mock_received_data)
        self.received_data = None

        # Stop the thread
        serial_thread.stop()
        serial_thread.wait()

        # Verify
        mock_serial_instance.open.assert_called_once()
        mock_serial_instance.close.assert_called_once()
        self.assertEqual(self.received_data, 'test data')

    def mock_received_data(self, data):
        """Mock function to capture received data."""
        self.received_data = data

if __name__ == '__main__':
    unittest.main()
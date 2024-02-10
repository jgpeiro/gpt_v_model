# integration_tests.py TEMPLATE
# This is a simplified example of integration tests for the Serial Terminal Application.
# It demonstrates basic testing of the integration between the GUI components and the SerialThread class.

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from unittest.mock import patch, MagicMock
from main import SerialTerminal, SerialThread

app = QApplication([])

class TestSerialTerminalIntegration(unittest.TestCase):
    """Integration tests for the Serial Terminal Application."""

    def setUp(self):
        """Set up the test environment."""
        self.serial_terminal = SerialTerminal()

    @patch.object(SerialThread, 'start')
    def test_open_serial_port(self, mock_start):
        """Test opening a serial port from the GUI."""
        # Simulate selecting a COM port and BAU rate, then clicking open
        self.serial_terminal.combo_com_ports.setCurrentIndex(0)
        self.serial_terminal.combo_baud_rate.setCurrentIndex(0)
        self.serial_terminal.btn_open.click()

        # Verify that SerialThread.start was called
        mock_start.assert_called_once()

    @patch.object(SerialThread, 'stop')
    def test_close_serial_port(self, mock_stop):
        """Test closing a serial port from the GUI."""
        # Simulate opening and then closing a serial port
        self.serial_terminal.open_serial_port()
        self.serial_terminal.btn_close.click()

        # Verify that SerialThread.stop was called
        mock_stop.assert_called_once()

    @patch('main.SerialThread')
    def test_send_data(self, mock_serial_thread):
        """Test sending data through the serial port from the GUI."""
        # Setup mock
        mock_instance = MagicMock()
        mock_serial_thread.return_value = mock_instance

        # Simulate opening a serial port
        self.serial_terminal.open_serial_port()

        # Simulate typing and sending data
        test_data = "Hello, World!"
        self.serial_terminal.line_input.setText(test_data)
        self.serial_terminal.btn_send.click()

        # Verify that SerialThread.serial_port.write was called with the correct data
        mock_instance.serial_port.write.assert_called_with((test_data + '\n').encode('utf-8'))

    def tearDown(self):
        """Tear down the test environment."""
        self.serial_terminal.close()

if __name__ == '__main__':
    unittest.main()
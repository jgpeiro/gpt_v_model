# system_tests.py TEMPLATE
# This is a simplified example of system tests for the Serial Terminal Application.
# It demonstrates basic testing of the application as a whole, focusing on user interactions and expected outcomes.

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from unittest.mock import patch, MagicMock
from main import SerialTerminal

app = QApplication([])

class TestSerialTerminalSystem(unittest.TestCase):
    """System tests for the Serial Terminal Application."""

    def setUp(self):
        """Set up the test environment."""
        self.serial_terminal = SerialTerminal()

    @patch('main.SerialThread')
    def test_full_interaction(self, mock_serial_thread):
        """Test full interaction with the application."""
        # Setup mock for SerialThread
        mock_instance = MagicMock()
        mock_serial_thread.return_value = mock_instance
        mock_instance.received.emit = MagicMock()

        # Simulate selecting COM port and BAU rate
        self.serial_terminal.combo_com_ports.setCurrentIndex(0)
        self.serial_terminal.combo_baud_rate.setCurrentIndex(0)

        # Simulate clicking the open button
        QTest.mouseClick(self.serial_terminal.btn_open, Qt.LeftButton)

        # Verify SerialThread was started
        mock_instance.start.assert_called_once()

        # Simulate typing and sending data
        test_data = "Hello, World!"
        self.serial_terminal.line_input.setText(test_data)
        QTest.mouseClick(self.serial_terminal.btn_send, Qt.LeftButton)

        # Verify data was sent
        mock_instance.serial_port.write.assert_called_with((test_data + '\n').encode('utf-8'))

        # Simulate receiving data
        received_data = "Received Data"
        mock_instance.received.emit(received_data)

        # Verify received data is displayed
        self.assertTrue(received_data in self.serial_terminal.text_display.toPlainText())

        # Simulate clicking the close button
        QTest.mouseClick(self.serial_terminal.btnClose, Qt.LeftButton)

        # Verify SerialThread was stopped
        mock_instance.stop.assert_called_once()

    def tearDown(self):
        """Tear down the test environment."""
        self.serial_terminal.close()

if __name__ == '__main__':
    unittest.main()
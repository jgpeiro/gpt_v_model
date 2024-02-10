# main.py TEMPLATE
# This is a simplified example of a Serial Terminal Application. It demonstrates the basic structure and functionality
# required to meet the specified requirements. This example focuses on GUI layout and basic serial communication functionality.

# Imports
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import serial.tools.list_ports

# Constants
BAUD_RATES = [9600, 19200, 38400, 57600, 115200]

# Logging setup for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Functions
def list_com_ports():
    """List available COM ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Classes
class SerialThread(QThread):
    """Background thread for reading serial data."""
    received = pyqtSignal(str)

    def __init__(self, port, baud_rate):
        super().__init__()
        self.serial_port = serial.Serial()
        self.serial_port.port = port
        self.serial_port.baudrate = baud_rate
        self.running = False

    def run(self):
        """Run the thread, reading data from the serial port."""
        self.serial_port.open()
        self.running = True
        while self.running:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.received.emit(data)
        self.serial_port.close()

    def stop(self):
        """Stop the thread."""
        self.running = False

class SerialTerminal(QMainWindow):
    """Main window class for the Serial Terminal Application."""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_thread = None

    def initUI(self):
        """Initialize the UI."""
        self.setWindowTitle('Serial Terminal')
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        layout = QVBoxLayout()

        # COM port selection
        self.combo_com_ports = QComboBox()
        self.combo_com_ports.addItems(list_com_ports())
        layout.addWidget(self.combo_com_ports)

        # BAUD rate selection
        self.combo_baud_rate = QComboBox()
        self.combo_baud_rate.addItems(map(str, BAUD_RATES))
        layout.addWidget(self.combo_baud_rate)

        # Open and close buttons
        self.btn_open = QPushButton('Open')
        self.btn_open.clicked.connect(self.open_serial_port)
        layout.addWidget(self.btn_open)

        self.btn_close = QPushButton('Close')
        self.btn_close.clicked.connect(self.close_serial_port)
        layout.addWidget(self.btn_close)

        # Terminal display
        self.text_display = QTextEdit()
        layout.addWidget(self.text_display)

        # Input field
        self.line_input = QLineEdit()
        layout.addWidget(self.line_input)

        # Send button
        self.btn_send = QPushButton('Send')
        self.btn_send.clicked.connect(self.send_data)
        layout.addWidget(self.btn_send)

        # Set main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_serial_port(self):
        """Open the selected serial port."""
        port = self.combo_com_ports.currentText()
        baud_rate = int(self.combo_baud_rate.currentText())
        self.serial_thread = SerialThread(port, baud_rate)
        self.serial_thread.received.connect(self.display_data)
        self.serial_thread.start()
        logging.info(f"Opened serial port {port} at {baud_rate} BAUD.")

    def close_serial_port(self):
        """Close the open serial port."""
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None
            logging.info("Closed serial port.")

    def send_data(self):
        """Send data through the serial port."""
        if self.serial_thread and self.serial_thread.serial_port.is_open:
            data = self.line_input.text() + '\n'
            self.serial_thread.serial_port.write(data.encode('utf-8'))
            self.display_data(data, sent=True)
            self.line_input.clear()
            logging.info("Sent data.")

    def display_data(self, data, sent=False):
        """Display received data in the terminal area."""
        if sent:
            self.text_display.append(f"<font color='green'>{data}</font>")
        else:
            self.text_display.append(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = SerialTerminal()
    mainWin.show()
    sys.exit(app.exec_())
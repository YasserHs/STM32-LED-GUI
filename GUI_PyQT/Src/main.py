# main.py
import sys
from PyQt5.QtWidgets import QApplication
from include.led_controller_ui import LEDController
from include.serial_communication import SerialCommunication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDController()  # Create LEDController first
    serial_comm = SerialCommunication(window)  # Pass LEDController to SerialCommunication
    window.serial_comm = serial_comm  # Assign serial_comm to LEDController
    window.show()
    sys.exit(app.exec_())
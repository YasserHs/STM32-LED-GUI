# serial_communication.py
import serial
import struct
import threading
from time import sleep
from PyQt5.QtWidgets import QMessageBox  # Added import

class SerialCommunication:
    def __init__(self, led_controller):
        self.led_controller = led_controller

    def reset_stm32(self):
        port_name = self.led_controller.serial_input.text().strip()
        if not port_name:
            QMessageBox.warning(self.led_controller, "Error", "Please enter a valid serial port!")
            return

        try:
            self.led_controller.serial_port = serial.Serial(port_name, 115200, timeout=1)
        except Exception as e:
            QMessageBox.critical(self.led_controller, "Error", f"Failed to connect to {port_name}: {str(e)}")
            self.led_controller.serial_port = None
            return

        self.send_to_stm32(b"Reset")
        if self.led_controller.serial_port and self.led_controller.serial_port.is_open:
            self.led_controller.serial_port.close()

    def send_configuration(self):
        port_name = self.led_controller.serial_input.text().strip()
        if not port_name:
            QMessageBox.warning(self.led_controller, "Error", "Please enter a valid serial port!")
            return

        try:
            self.led_controller.serial_port = serial.Serial(port_name, 115200, timeout=1)
        except Exception as e:
            QMessageBox.critical(self.led_controller, "Error", f"Failed to connect to {port_name}: {str(e)}")
            self.led_controller.serial_port = None
            return

        for idx, (color, data) in enumerate(self.led_controller.leds.items(), start=1):
            if data["state"]:
                state = 1 if data["state"] else 0
                time_ms = data["time_ms"]
                packed_data = struct.pack("<LBB", time_ms, idx, state)
                print(f"Sending to LED {idx}: State={state}, Time={time_ms} ms")
                self.send_to_stm32(packed_data)

        self.send_to_stm32(b"end")
        if self.led_controller.serial_port and self.led_controller.serial_port.is_open:
            self.led_controller.serial_port.close()

    def send_to_stm32(self, data):
        with self.led_controller.lock:
            if self.led_controller.serial_port and self.led_controller.serial_port.is_open:
                try:
                    for attempt in range(3):
                        try:
                            self.led_controller.serial_port.write(data)
                            self.led_controller.serial_port.flush()
                            print(f"Sent: {data}")
                            return
                        except serial.SerialException as e:
                            print(f"Attempt {attempt + 1} failed: {str(e)}")
                            sleep(0.5)
                    raise serial.SerialException("Failed to send data after 3 attempts")
                except serial.SerialException as e:
                    QMessageBox.critical(self.led_controller, "Error", f"Failed to send data: {str(e)}")
                    self.led_controller.serial_port.close()
                    self.led_controller.serial_port = None
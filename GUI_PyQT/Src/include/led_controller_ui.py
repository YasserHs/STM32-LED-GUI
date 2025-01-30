# led_controller_ui.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QColor
import json
import threading

class LEDController(QWidget):
    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.lock = threading.Lock()
        self.serial_comm = None  # Will be set later
        self.initUI()

    def initUI(self):
        self.setWindowTitle("STM32 LED CONTROLLER")
        resolution = QApplication.desktop().screenGeometry()  # Get screen resolution
        x = int((resolution.width() / 2) - (self.frameSize().width() / 2))  # Convert to int
        y = int((resolution.height() / 2) - (self.frameSize().height() / 2))  # Convert to int
        self.setGeometry(x, y, 500, 400)  # Set the window geometry with calculated x and y

        layout = QVBoxLayout()

        # Serial Port Input (Editable)
        serial_layout = QHBoxLayout()
        serial_label = QLabel("Serial Port:")
        self.serial_input = QLineEdit("/dev/ttyACM1")  # Default value
        self.serial_input.setPlaceholderText("e.g., /dev/ttyACM1")
        serial_layout.addWidget(serial_label)
        serial_layout.addWidget(self.serial_input)
        layout.addLayout(serial_layout)

        # LED Controls
        self.leds = {
            "Red": {"button": None, "input": None, "label": None, "color": QColor(255, 0, 0), "state": False, "time_ms": 0},
            "Green": {"button": None, "input": None, "label": None, "color": QColor(0, 255, 0), "state": False, "time_ms": 0},
            "Blue": {"button": None, "input": None, "label": None, "color": QColor(0, 0, 255), "state": False, "time_ms": 0},
            "Orange": {"button": None, "input": None, "label": None, "color": QColor(255, 165, 0), "state": False, "time_ms": 0},
        }

        for idx, color in enumerate(self.leds.keys(), start=1):  # Start LED indices from 1
            hbox = QHBoxLayout()

            # LED Button
            button = QPushButton(f"{color} LED")
            button.setStyleSheet(f"background-color: {self.leds[color]['color'].name()}")
            button.setCheckable(True)
            button.toggled.connect(lambda state, c=color: self.toggle_led(state, c))
            self.leds[color]["button"] = button

            # Time Input
            time_input = QLineEdit()
            time_input.setPlaceholderText("Cycle (ms)")
            time_input.textChanged.connect(lambda text, c=color: self.update_delay(c, text))
            self.leds[color]["input"] = time_input

            # On/Off Indicator
            status_label = QLabel("Off")
            self.leds[color]["label"] = status_label

            # Add Widgets to Layout
            hbox.addWidget(button)
            hbox.addWidget(time_input)
            hbox.addWidget(status_label)
            layout.addLayout(hbox)

        # Buttons for saving, loading, and sending configurations
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_configuration)
        load_button = QPushButton("Load Configuration")
        load_button.clicked.connect(self.load_configuration)
        send_button = QPushButton("Send Configuration")
        send_button.clicked.connect(self.send_configuration)

        reset_button = QPushButton("Reset the STM32")
        reset_button.clicked.connect(self.reset_stm32)

        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        button_layout.addWidget(send_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def toggle_led(self, state, color):
        self.leds[color]["state"] = state
        self.leds[color]["label"].setText("On" if state else "Off")

    def update_delay(self, color, text):
        try:
            self.leds[color]["time_ms"] = int(text) if text else 0
        except ValueError:
            self.leds[color]["time_ms"] = 0

    def save_configuration(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", "JSON Files (*.json)", options=options)
        
        if file_path:
            if not file_path.lower().endswith(".json"):
                file_path += ".json"

            config = {
                f"LED{idx}": {"state": data["state"], "time_ms": data["time_ms"]}
                for idx, (color, data) in enumerate(self.leds.items(), start=1)
                if data["state"]
            }

            with open(file_path, "w") as file:
                json.dump(config, file, indent=4)
            QMessageBox.information(self, "Saved", f"Configuration saved to {file_path}.")


    def load_configuration(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json)", options=options)
        if file_path:
            try:
                with open(file_path, "r") as file:
                    config = json.load(file)
                print("Loaded Configuration:")
                print(json.dumps(config, indent=4))

                # Reset all labels and inputs to their default state before loading new data
                for led_name, led_data in self.leds.items():
                    led_data["label"].setText("Off")  # Reset label to "Off"
                    led_data["button"].setChecked(False)  # Uncheck the button
                    led_data["input"].setText("")  # Clear the input field

                # Load the new configuration
                for led_name, led_data in config.items():
                    idx = int(led_name.replace("LED", "")) - 1
                    color = list(self.leds.keys())[idx]

                    self.leds[color]["state"] = led_data["state"]
                    self.leds[color]["button"].setChecked(led_data["state"])
                    self.leds[color]["label"].setText("On" if led_data["state"] else "Off")

                    self.leds[color]["time_ms"] = led_data["time_ms"]
                    self.leds[color]["input"].setText(str(led_data["time_ms"]))

                QMessageBox.information(self, "Loaded", f"Configuration loaded from {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")

    def send_configuration(self):
        if self.serial_comm:
            self.serial_comm.send_configuration()
        else:
            QMessageBox.critical(self, "Error", "Serial communication not initialized!")

    def reset_stm32(self):
        if self.serial_comm:
            self.serial_comm.reset_stm32()
        else:
            QMessageBox.critical(self, "Error", "Serial communication not initialized!")

    def closeEvent(self, event):
        # Ask the user if they want to close the application
        reply = QMessageBox.question(
            self, "Exit", "Are you sure you want to close the application?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            event.accept()
        else:
            event.ignore()


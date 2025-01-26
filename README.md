# STM32 USB-OTG LED Control Project
A project to control LEDs connected to an STM32 microcontroller via a desktop GUI. The STM32 firmware communicates with the GUI using USB OTG, allowing users to turn LEDs on/off and set a specific toggle frequency for dynamic lighting effects.

---

## **Project Overview**
The STM32 microcontroller is configured to:
1. Enable GPIO pins for controlling LEDs.
2. Activate USB-OTG in device mode using the `USB_OTG_FS` peripheral.
3. Use the Virtual COM Port (VCP) middleware to communicate with a host device (e.g., a PC) over USB.

---

## **Hardware Requirements**
- STM32 microcontroller with USB-OTG support (e.g., STM32F4 series).
- LEDs connected to GPIO pins.
- USB cable for connecting the STM32 to a host device (e.g., PC).

---

## **Software Requirements**
- STM32CubeMX for configuration and code generation.
- IDE for development (e.g., STM32CubeIDE, Keil, or VSCode).
- USB drivers for Virtual COM Port (usually installed automatically by the OS).

---

## **Configuration Steps**

### 1. GPIO Configuration for LEDs
- Open STM32CubeMX and select your STM32 microcontroller.
- Navigate to the **GPIO** settings.
- Configure the GPIO pins connected to the LEDs as **Output** mode.

### 2. USB-OTG Configuration
- In STM32CubeMX, go to the **Connectivity** section.
- Enable **USB_OTG_FS** in **Device Only** mode.
- Configure the USB settings (leave as default).

### 3. Middleware Configuration (Virtual COM Port)
- In STM32CubeMX, go to the **Middleware** section.
- Enable **USB_DEVICE** and select **Communication Device Class (Virtual COM Port)**.

### 4. Generate Code
- Click **Project Manager** and configure the toolchain/IDE settings (in this case, CMake is used for VSCode).
- Generate the code by clicking **Generate Code**.

---

## **Building and Flashing**

### 1. Generate Makefile and Create Build Folder
Run the following command to generate the Makefile and create the build folder:
```bash
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE=./cmake/gcc-arm-none-eabi.cmake -S./ -B./build/Debug -G "Unix Makefiles"
```

### 2. Build the Project
Build the project using the following command:
```bash
make
```
This will compile the code and generate the binary files in the `build/debug` folder.

### 3. Flash the Firmware
Flash the firmware to your STM32 board using:
```bash
make upload
```
This will flash the code from the `build/debug` folder to your STM32 microcontroller.

### 4. Connect the STM32 to the Host
Connect the STM32 to your PC via USB. Ensure that the Virtual COM Port driver is properly installed to enable communication.

---

## **Usage**
1. Open a terminal application on your PC (e.g., PuTTY, Tera Term).
2. Connect to the Virtual COM Port assigned to the STM32.
3. Send commands through the terminal to control the LEDs on the STM32 board.

---

## **Notes**
- Ensure the USB cable supports data transfer (not just charging).
- Test the communication with a basic terminal command like "Hello World" to verify USB-OTG functionality.
- Use appropriate resistor values for LEDs to avoid damaging the GPIO pins.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

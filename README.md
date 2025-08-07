# Smart Buoy

An Arduino-based smart buoy system that logs temperature, light intensity, and orientation data to an SD card for environmental and oceanographic monitoring.

## Features

- Reads sensor data from:
  - DS18B20 (Temperature)
  - BH1750 (Ambient Light)
  - MPU6050 (Pitch, Roll, Yaw)
- Stores data to an SD card in human-readable format
- Adds "NEW ENTRY" markers for each new logging session
- Serial monitor output for live sensor readings
- Easily extensible for further enhancements

## Data Format

### Logged Output (Text)
NEW ENTRY
T: 76.45F | L: 350.23 lx | Pitch: 1.23 | Roll: -0.67 | Yaw: 89.56
T: 76.51F | L: 352.10 lx | Pitch: 1.28 | Roll: -0.62 | Yaw: 89.60
...

markdown
Copy
Edit

Each reading is timestamped implicitly by order, logged every 2 seconds.

## Setup Instructions

### Hardware Required

- Arduino Uno / Nano / Mega
- DS18B20 Temperature Sensor
- BH1750 Light Sensor
- MPU6050 Accelerometer & Gyroscope
- Micro SD Card Module + SD Card
- 4.7kΩ resistor (for DS18B20 data line)
- Breadboard and jumper wires
- Battery pack + Solar panel

### Wiring Overview

| Component       | Pin Connections                        |
|----------------|-----------------------------------------|
| **BH1750**      | VCC → 5V, GND → GND, SDA → A4, SCL → A5 |
| **MPU6050**     | VCC → 5V, GND → GND, SDA → A4, SCL → A5 |
| **DS18B20**     | Data → D2, VCC → 5V, GND → GND (4.7kΩ pull-up to 5V) |
| **SD Module**   | CS → D10, MOSI → D11, MISO → D12, SCK → D13, VCC → 5V, GND → GND |

## Requirements

- Arduino IDE
- Libraries (install via Library Manager):
  - `BH1750 by Christopher Laws`
  - `MPU6050_light by rfetick`
  - `OneWire by Paul Stoffregen`
  - `DallasTemperature by Miles Burton`
  - `SD` (built-in)
  - `SPI` (built-in)
  - `Wire` (built-in)

## Example Output (Serial Monitor)

T: 76.45F | L: 350.23 lx | Pitch: 1.23 | Roll: -0.67 | Yaw: 89.56
Data written to file.


## Files and Folders

- `ocean_logger.ino` - Main Arduino sketch
- `requirements.txt` - Arduino libraries list
- `README.md` - This documentation
- `Converter` - Script to convert data to Json     

## Future Work

Planned enhancements to improve functionality and robustness:

### ✅ System Ready LED Indicator
Add an LED that turns on when all sensors and the SD card are initialized correctly, providing a visual “ready” status.

### 🌐 Wireless Logging
Incorporate an ESP8266/ESP32 or LoRa module to transmit sensor data wirelessly for remote access.

### 💤 Low Power Mode
Enable sleep mode to conserve battery during idle periods or use timed wake intervals.

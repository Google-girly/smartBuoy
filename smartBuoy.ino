#include <Wire.h>
#include <BH1750.h>
#include <MPU6050_light.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SD.h>
#include <SPI.h>

// ----- Sensors -----
BH1750 lightMeter;
MPU6050 mpu(Wire);
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);

// ----- SD Card -----
const int CS_PIN = 10;
File file;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  pinMode(CS_PIN, OUTPUT);

  // Initialize sensors and test for sensor failure
  if (lightMeter.begin()) Serial.println("BH1750 initialized.");
  else Serial.println("BH1750 failed.");

  mpu.begin();
  Serial.println("Calibrating MPU6050...");
  delay(1000);
  mpu.calcOffsets();
  Serial.println("MPU6050 ready.");

  tempSensor.begin();
  Serial.println("DS18B20 ready.");

  // Initialize SD card and test for SD failure
  Serial.println("Initializing SD card...");
  if (SD.begin()) {
    Serial.println("SD card is ready to use.");

    // Create file and write header
    file = SD.open("oceanLog.txt", FILE_WRITE);
    if (file) {
      // Creates a distinction in new entrys when file is appended
      file.println("NEW ENTRY");
      file.close();
      Serial.println("Header written successfully.");
    } else {
      Serial.println("Failed to create and write to oceanLog.txt");
    }

    delay(2000); // Allow SD card to recover before loop starts

  } else {
    Serial.println("SD card initialization failed.");
    return;
  }
}

void loop() {
  // Read sensors
  mpu.update();
  float lux = lightMeter.readLightLevel();
  tempSensor.requestTemperatures();
  float tempC = tempSensor.getTempCByIndex(0);
  float tempF = tempC * 9.0 / 5.0 + 32.0;
  float pitch = mpu.getAngleX();
  float roll = mpu.getAngleY();
  float yaw = mpu.getAngleZ();

  // Create log line
  String logLine = "T: " + String(tempF, 2) + "F | ";
  logLine += "L: " + String(lux, 2) + " lx | ";
  logLine += "Pitch: " + String(pitch, 2);
  logLine += " | Roll: " + String(roll, 2);
  logLine += " | Yaw: " + String(yaw, 2);

  // Print to Serial for testing
  Serial.println(logLine);

  delay(50); // Brief delay before SD access to prevent crashes

  // Write to SD card
  file = SD.open("oceanLog.txt", FILE_WRITE);
  if (file) {
    file.println(logLine);
    file.close();
    Serial.println("Data written to file.");
  } else {
    Serial.println("Failed to open oceanLog.txt");
  }

  delay(2000); // Reduce write frequency to ease SD load
}

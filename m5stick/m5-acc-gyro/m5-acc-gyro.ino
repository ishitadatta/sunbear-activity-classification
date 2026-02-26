#include <M5StickCPlus2.h>
#include <FS.h>
#include <LittleFS.h>

const char* LOG_FILE = "/log.csv";
bool isRecording = false; // State variable to track recording status

// --- Utility Functions ---

void setRecordingIndicator(bool on) {
  M5.Power.setLed(on ? 1 : 0);
}

void updateStatusDisplay() {
  M5.Lcd.setCursor(0, 100); // Display the status lower on the screen
  M5.Lcd.setTextColor(WHITE, BLACK);
  if (isRecording) {
    M5.Lcd.println("STATUS: RECORDING...");
  } else {
    M5.Lcd.println("STATUS: STANDBY. Press A to start.");
  }
}

// --- Setup ---

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextFont(2);
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setCursor(0, 0); 
  
  // 1. Initialize LittleFS
  if (!LittleFS.begin(true)) {
    M5.Lcd.println("LittleFS Mount Failed");
    while (1) delay(100); 
  }
  M5.Lcd.println("LittleFS OK");

  // 3. Write CSV Header (only if file is new/empty)
  File file = LittleFS.open(LOG_FILE, "a");
  if (file) {
    if (file.size() == 0) { 
        // --- UPDATED CSV HEADER TO INCLUDE GYRO DATA ---
        file.println("AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ");
    }
    file.close();
  }
  
  setRecordingIndicator(false); // Start in standby mode (LED OFF)
  updateStatusDisplay();
}

// --- Main Loop ---

void loop() {
  // Update button state once per loop
  M5.update(); 
  
  // Check if Button A was pressed
  if (M5.BtnA.wasPressed()) {
    isRecording = !isRecording; // Toggle the state
    setRecordingIndicator(isRecording); // Turn LED ON/OFF
    updateStatusDisplay(); // Update the display text
    
    // Optional: Log the start/stop event to the file
    File file = LittleFS.open(LOG_FILE, "a");
    if (file) {
        if (isRecording) {
            file.println("--- RECORDING STARTED ---");
        } else {
            file.println("--- RECORDING STOPPED ---");
        }
        file.close();
    }
  }

  // Read data whether recording or not, but only display/log if recording
  float ax, ay, az;
  float gx, gy, gz; // --- DECLARE GYRO VARIABLES ---
  
  M5.Imu.getAccelData(&ax, &ay, &az);
  M5.Imu.getGyroData(&gx, &gy, &gz); // --- READ GYRO DATA ---
  
  // Display only Accel data to save screen space, or you can adjust the display logic
  M5.Lcd.setCursor(0, 40);
  M5.Lcd.printf("Accel: %.2f, %.2f, %.2f  ", ax, ay, az); 
  M5.Lcd.setCursor(0, 60);
  M5.Lcd.printf("Gyro:  %.2f, %.2f, %.2f  ", gx, gy, gz); // Displaying Gyro data

  if (isRecording) {
    // --- Log Data to File ---
    File file = LittleFS.open(LOG_FILE, "a");
    if (file) {
      // --- UPDATED DATA STRING TO INCLUDE GYRO DATA ---
      String dataString = String(ax, 2) + "," + String(ay, 2) + "," + String(az, 2)
                        + "," + String(gx, 2) + "," + String(gy, 2) + "," + String(gz, 2);
                        
      file.println(dataString);
      file.close();
    } else {
      M5.Lcd.setCursor(0, 80);
      M5.Lcd.println("File Write FAILED!");
    }
  }
  
  delay(500); // Half-second interval
}
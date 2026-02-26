#include <M5StickCPlus2.h>
#include <FS.h>
#include <LittleFS.h>
#include <time.h> 

const char* LOG_FILE = "/log.csv";
bool isRecording = false; 

// --- Utility Functions ---

void setRecordingIndicator(bool on) {
  M5.Power.setLed(on ? 1 : 0);
}

void updateStatusDisplay() {
  M5.Lcd.setCursor(0, 130); 
  M5.Lcd.setTextColor(WHITE, BLACK);
  
  // Clear the status line before printing the new status
  M5.Lcd.fillRect(0, 130, M5.Lcd.width(), 20, BLACK); 

  M5.Lcd.setCursor(0, 130);
  M5.Lcd.print("STATUS: ");
  if (isRecording) {
    M5.Lcd.println("RECORDING...");
  } else {
    M5.Lcd.println("STANDBY. Press A to start.");
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
  
  // 2. Initialize IMU
  M5.Imu.begin(); 
  M5.Lcd.println("IMU initialized.");
  
  // 3. --- Initialize and Set RTC Time using standard struct tm ---
  struct tm t;
  // Current time: Wednesday, November 12, 2025 at 10:01:00 PM EST
  t.tm_year  = 2025 - 1900; 
  t.tm_mon   = 10;          
  t.tm_mday  = 12;          
  t.tm_hour  = 22;          
  t.tm_min   = 01;          
  t.tm_sec   = 0;           
  M5.Rtc.setDateTime(t);
  M5.Lcd.println("RTC Set.");
  // ------------------------------------

  // 4. Write CSV Header 
  File file = LittleFS.open(LOG_FILE, "a");
  if (file) {
    if (file.size() == 0) { 
        file.println("Timestamp,AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ");
    }
    file.close();
  }
  
  setRecordingIndicator(false); 
  updateStatusDisplay();
}

// --- Main Loop ---

void loop() {
  M5.update(); 
  
  // Check if Button A was pressed (Toggle Recording)
  if (M5.BtnA.wasPressed()) {
    isRecording = !isRecording; 
    setRecordingIndicator(isRecording); 
    updateStatusDisplay(); 
    
    // Log the start/stop event
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

  // Read Sensor Data
  float ax, ay, az;
  float gx, gy, gz; 
  M5.Imu.getAccelData(&ax, &ay, &az);
  M5.Imu.getGyroData(&gx, &gy, &gz); 
  
  // Get current Time using the CORRECT types indicated by the compiler error
  m5::rtc_date_t DateStruct;
  m5::rtc_time_t TimeStruct;
  M5.Rtc.getDateTime(&DateStruct, &TimeStruct); 

  // Format the timestamp string (YYYY-MM-DD HH:MM:SS)
  // Fields are now lowercase (year, month, date, hours, minutes, seconds)
  String timestamp = String(DateStruct.year) + "-" + 
                     String(DateStruct.month) + "-" + 
                     String(DateStruct.date) + " " + 
                     String(TimeStruct.hours) + ":" + 
                     String(TimeStruct.minutes) + ":" + 
                     String(TimeStruct.seconds);

  // Display Sensor Data and Time
  M5.Lcd.setCursor(0, 40);
  M5.Lcd.printf("Time: %s", timestamp.c_str());
  M5.Lcd.setCursor(0, 60);
  M5.Lcd.printf("Accel: %.2f, %.2f, %.2f", ax, ay, az); 
  M5.Lcd.setCursor(0, 80);
  M5.Lcd.printf("Gyro: %.2f, %.2f, %.2f", gx, gy, gz); 
  

  if (isRecording) {
    // Log Data to File
    File file = LittleFS.open(LOG_FILE, "a");
    if (file) {
      String dataString = timestamp + "," +  
                          String(ax, 2) + "," + String(ay, 2) + "," + String(az, 2) + "," + 
                          String(gx, 2) + "," + String(gy, 2) + "," + String(gz, 2);
                        
      file.println(dataString);
      file.close();
    } 
  }
  
  delay(500); 
}
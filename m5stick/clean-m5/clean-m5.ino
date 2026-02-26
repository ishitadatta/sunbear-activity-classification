#include <M5StickCPlus2.h>
#include <LittleFS.h>
#include <FS.h>

const char* LOG_FILE = "/log.csv";

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextFont(2);
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setCursor(0, 0); 
  
  M5.Lcd.println("--- LOG CLEANER ---");
  
  // 1. Initialize LittleFS
  if (!LittleFS.begin(false)) { // 'false' prevents accidental formatting of the chip
    M5.Lcd.setTextColor(RED, BLACK);
    M5.Lcd.println("LittleFS Mount Failed!");
    M5.Lcd.setTextColor(WHITE, BLACK);
    return; // Exit setup if mount fails
  }
  M5.Lcd.println("LittleFS Mounted.");
  
  // 2. Check and Delete the File
  M5.Lcd.println("Checking for log.csv...");

  if (LittleFS.exists(LOG_FILE)) {
    M5.Lcd.println("File found. Deleting...");
    
    if (LittleFS.remove(LOG_FILE)) {
      M5.Lcd.setTextColor(GREEN, BLACK);
      M5.Lcd.println("SUCCESS: Log file deleted!");
    } else {
      M5.Lcd.setTextColor(RED, BLACK);
      M5.Lcd.println("ERROR: File deletion failed!");
    }
  } else {
    M5.Lcd.setTextColor(YELLOW, BLACK);
    M5.Lcd.println("Log file not found. Nothing to delete.");
  }
  
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setCursor(0, 100);
  M5.Lcd.println("Operation complete. Device is idle.");
  
  // Turn off the LED just in case
  M5.Power.setLed(0);
}

void loop() {
  // We keep the loop empty so the device just holds the final status message.
  delay(100);
}
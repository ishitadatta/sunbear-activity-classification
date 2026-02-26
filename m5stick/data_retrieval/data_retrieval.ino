#include <FFat.h>

#include <M5StickCPlus2.h>

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);

  // Initialize the screen
  M5.Lcd.setRotation(1);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextColor(MAGENTA);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(10, 10);
  M5.Lcd.println("PLUS2 UART TEST");

  // Red Port (Port A) Pins
  Serial1.begin(115200, SERIAL_8N1, 33, 32);
}

void loop() {
  M5.update();

  // Blink internal LED to show the chip isn't frozen
  static uint32_t last_blink = 0;
  if (millis() - last_blink > 500) {
    last_blink = millis();
    // In Plus2, the LED is on Pin 19
    digitalWrite(19, !digitalRead(19)); 
  }

  // Monitor UART
  while (Serial1.available()) {
    char c = Serial1.read();
    M5.Lcd.print(c);
    
    // Auto-clear logic
    if (M5.Lcd.getCursorY() > M5.Lcd.height() - 20) {
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setCursor(0, 0);
    }
  }
}
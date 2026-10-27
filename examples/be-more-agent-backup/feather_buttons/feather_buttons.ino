// Adafruit Feather 32u4 Basic Proto. Native Arduino Keyboard library.
// Connect each listed input to GND through its own momentary switch.
// Hold button 7 during power-on for diagnostic-only mode (no HID key output).
// These keys control the foreground desktop app, NEVER wheels.
#include <Keyboard.h>
const uint8_t pins[] = {5, 6, 10, 11, 12, A0, A1};
const uint8_t keys[] = {KEY_RETURN, ' ', KEY_ESC, 0, 0, 0, 0};
bool stable[7], lastRead[7]; unsigned long changed[7];
bool hidEnabled = false;
void setup() {
  Serial.begin(115200);
  for (uint8_t i=0; i<7; i++) {
    pinMode(pins[i], INPUT_PULLUP);
    stable[i]=lastRead[i]=digitalRead(pins[i]); changed[i]=millis();
  }
  hidEnabled = digitalRead(A1)==HIGH;
  if (hidEnabled) Keyboard.begin();
}
void loop() {
  unsigned long now=millis();
  for (uint8_t i=0; i<7; i++) {
    bool value=digitalRead(pins[i]);
    if (value!=lastRead[i]) { lastRead[i]=value; changed[i]=now; }
    if (value!=stable[i] && (unsigned long)(now-changed[i])>=30) {
      stable[i]=value;
      if (!value) {
        // Finite press/release, not a held key. Unassigned buttons only report an event.
        if (hidEnabled && keys[i]) Keyboard.write(keys[i]);
        if (Serial && Serial.availableForWrite()>=32) {
          Serial.print("{\"button\":"); Serial.print(i+1); Serial.println("}");
        }
      }
    }
  }
  delay(2);
}

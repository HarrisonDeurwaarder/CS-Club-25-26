/*

 LCD Pin | Name | Connect to Arduino
------------------------------------
 1      | GND  | GND
 2      | VCC  | 5V
 3      | VO   | Middle of 10k pot (contrast)
 4      | RS   | D12
 5      | RW   | GND
 6      | EN   | D11
 7      | D0   | (leave unconnected)
 8      | D1   | (leave unconnected)
 9      | D2   | (leave unconnected)
10      | D3   | (leave unconnected)
11      | D4   | D5
12      | D5   | D4
13      | D6   | D3
14      | D7   | D2
15      | LED+ | 5V (with 220Ω resistor in series)
16      | LED- | GND

Potentiometer
---------------
Left pin  → 5V
Middle pin → LCD Pin 3 (VO)
Right pin → GND

Buttons
---------------
Left button:   one leg → D6,   other leg → GND
Middle button: one leg → D7,   other leg → GND
Right button:  one leg → D8,   other leg → GND


*/

#include <LiquidCrystal.h>  
// This library lets the Arduino control a standard 16×2 LCD
// using 6 digital pins.


// ------------------------------------------------------------
// LCD SETUP
// ------------------------------------------------------------
// LiquidCrystal(rs, enable, d4, d5, d6, d7)
// These pin numbers MUST match your wiring.
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


// ------------------------------------------------------------
// BUTTON PINS
// ------------------------------------------------------------
// We will use INPUT_PULLUP so the buttons connect to GROUND.
// That means: NOT pressed = HIGH, pressed = LOW.
const int leftBtn  = 6;
const int midBtn   = 7;
const int rightBtn = 8;


// ------------------------------------------------------------
// GAME STATE VARIABLES
// ------------------------------------------------------------
int score = 0;                  // Player score
unsigned long lastMoleTime = 0; // When the last mole event happened
int molePos = -1;               // Mole location: 0,1,2 or -1 meaning none
unsigned long moleInterval = 1500; // How long the mole stays alive (ms)
bool moleActive = false;        // Whether a mole is currently showing


void setup() {
  // ------------------------------------------------------------
  // LCD INITIALIZATION
  // ------------------------------------------------------------
  lcd.begin(16, 2);   // 16 chars per line, 2 lines
  
  // ------------------------------------------------------------
  // BUTTON INITIALIZATION
  // ------------------------------------------------------------
  // INPUT_PULLUP means Arduino uses an internal resistor to keep
  // the pin HIGH. When the button is pressed → pin goes LOW.
  pinMode(leftBtn,  INPUT_PULLUP);
  pinMode(midBtn,   INPUT_PULLUP);
  pinMode(rightBtn, INPUT_PULLUP);

  // Show a startup message
  lcd.print("Whack-A-Mole!");
  delay(1500);    // Pause for 1.5 seconds
  lcd.clear();    // Clear the screen before the game starts
}


void loop() {
  unsigned long now = millis();
  // millis() returns how many ms have passed since power-on.
  // It is used for timing instead of delays so the game runs smoothly.


  // ------------------------------------------------------------
  // MOLE APPEARANCE LOGIC
  // ------------------------------------------------------------
  // Spawn a new mole when:
  // 1. No mole is active
  // 2. Enough time has passed since the last mole event
  if (!moleActive && now - lastMoleTime > moleInterval) {
    molePos = random(0, 3); // pick 0, 1, or 2 randomly
    drawMole(molePos);       // show it on the LCD
    moleActive = true;       // now a mole exists
    // NOTE: lastMoleTime is NOT updated here, only when the mole ends
  }


  // ------------------------------------------------------------
  // CHECK BUTTON PRESSES (HIT DETECTION)
  // ------------------------------------------------------------
  if (moleActive) {
    // If the correct button for that position is pressed, call hit().
    // pressed(pin) returns true if pin == LOW.
    if (pressed(leftBtn)  && molePos == 0) hit();
    if (pressed(midBtn)   && molePos == 1) hit();
    if (pressed(rightBtn) && molePos == 2) hit();

    // ------------------------------------------------------------
    // MISS LOGIC
    // ------------------------------------------------------------
    // If too much time passes while the mole is active → miss.
    // This checks if the mole has lived longer than the interval.
    if (now - lastMoleTime > moleInterval) {
      miss();
    }
  }
}


// ------------------------------------------------------------
// HELPER FUNCTION: Detect Button Press
// ------------------------------------------------------------
// Because of INPUT_PULLUP: HIGH = not pressed, LOW = pressed.
bool pressed(int pin) {
  return digitalRead(pin) == LOW;
}


// ------------------------------------------------------------
// HELPER FUNCTION: Draw the Mole
// ------------------------------------------------------------
// pos will be 0, 1, or 2. We spread them out across the LCD
// by multiplying by 5 (rough spacing across a 16-character row).
void drawMole(int pos) {
  lcd.clear();
  lcd.setCursor(pos * 5, 0); // Column, Row
  lcd.print("M");            // Print the mole as "M"
}


// ------------------------------------------------------------
// HELPER FUNCTION: Handle a Hit
// ------------------------------------------------------------
void hit() {
  score++;                    // Increase score
  moleActive = false;         // Remove mole
  lastMoleTime = millis();    // Reset mole timer

  // Show hit feedback
  lcd.setCursor(0, 1);
  lcd.print("Hit! Score:");
  lcd.print(score);

  delay(400);   // Short pause for feedback
  lcd.clear();  // Clean screen for next mole
}


// ------------------------------------------------------------
// HELPER FUNCTION: Handle a Miss
// ------------------------------------------------------------
void miss() {
  moleActive = false;         // Mole is gone now
  lastMoleTime = millis();    // Reset the timer

  // Show miss feedback
  lcd.setCursor(0, 1);
  lcd.print("Miss! Score:");
  lcd.print(score);

  delay(400);
  lcd.clear();
}
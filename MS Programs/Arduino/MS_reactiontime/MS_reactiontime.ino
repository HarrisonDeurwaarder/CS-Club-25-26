// Save the pins that we will use later (as CONSTANT variables)
const int ledPin = 13;
const int buttonPin = 2;

// Save the time that the game STARTS
// "unsigned" just means that startTime can only be positive
unsigned int startTime = 0;
// Keep track of whether the user has CLICKED THE BUTTON or not
bool waitingForReaction = false;

void setup() {
    // Tell the arduino where which pins should take voltage as an INPUT
    // or send voltage as an OUTPUT
    pinMode(ledPin, OUTPUT);
    pinMode(buttonPin, INPUT_PULLUP);
    // Set up the console to print informatiion
    Serial.begin(9600);
    Serial.println("Reaction Time Game Ready!");
    // Delay the start of the game
    delay(2000);
}

void loop() {
    // Random delay before LED turns on
    // You can change this value if you'd like
    digitalWrite(ledPin, LOW);
    delay(random(2000, 5000));

    // Turn LED on and start timing
    digitalWrite(ledPin, HIGH);
    startTime = millis();
    waitingForReaction = true;

    // While we're still waiting, constantly check if the button is clicked
    while (waitingForReaction) {
        // Check the state of the button
        if (digitalRead(buttonPin) == LOW) {  // Button pressed
        // Find the distance between when the timer STARTED vs. when the user CLICKED THE BUTTON
        unsigned long reactionTime = millis() - startTime;
        // Display the reaction time
        Serial.print("Reaction time: ");
        Serial.print(reactionTime);
        Serial.println(" ms");

        // Flash LED to indicate result
        for (int i = 0; i < 3; i++) {
            // LOW means the LED is off
            digitalWrite(ledPin, LOW);
            delay(200);
            // HIGH means the LED is on
            digitalWrite(ledPin, HIGH);
            delay(200);
        }

        // After processing, let the program know that we can continue through the program
        waitingForReaction = false;
        }
    }

    // Pause before next round
    // The game will continue until the arduino is turned off
    digitalWrite(ledPin, LOW);
    delay(2000);
}

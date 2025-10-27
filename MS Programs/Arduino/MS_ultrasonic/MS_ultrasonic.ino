// ultrasonic distance sensor measures distance, then prints

const int BUZZER_PIN = 8;
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;

void setup() {
  // put your setup code here, to run once:

  // tells the program where to display the text we give it (like print)
  Serial.begin(9600);
  // tells the program that the pin 9 (because we define TRIG_PIN as 9) is going to OUTPUT voltage for the sensor to interpret
  pinMode(TRIG_PIN, OUTPUT);
  // pin 10 will take voltages sent by the sensor as INPUT-- this tells us what the distance is!
  pinMode(ECHO_PIN, INPUT);
  // same logic as the above!
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  // send voltage to the sensor (tell it to start measuring distance)
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  // then tell it to stop
  digitalWrite(TRIG_PIN, LOW);

  // sensor ACTUALLY returns how long it took for the sonic waves to bounce back
  // we can convert that to distance easily!
  long duration = pulseIn(ECHO_PIN, HIGH);
  // we convert it to CM by multiplying by the speed of sound
  float distance = (duration * 0.0343) / 2; 

  // remember how we did Serial.begin()?
  // that's so we can print out to the console easily!
  Serial.println(distance);

  // lets send voltage to the buzzer based on the distance
  // clip the distance between 5 and 200
  float clippedDistance = constrain(distance, 5.0, 200.0);
  // turn the distance into a frequency that we can send to the 
  float frequency = (int) (1000.0 / (clippedDistance / 20.0));

  tone(BUZZER_PIN, frequency);

  delay(500);
}

/*
  Blinking LED project.
  Turns on an LED on for one second, then off for one second, repeatedly.
  Last Modification modified 30 March 2020
  by Roy Ben Avraham
 */
int i = 0;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(8, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  if (i == 0)
  {
    delay(10000);
    i++;
  }
  
  digitalWrite(8, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(100);              // wait for a second
  digitalWrite(8, LOW);    // turn the LED off by making the voltage LOW
  delay(100);              // wait for a second
}

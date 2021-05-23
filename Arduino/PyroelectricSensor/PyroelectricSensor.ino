int data;
int INPUTPIN = A0;
int OUTPUTPIN = 6;

void setup() {
  Serial.begin(115200);
}

void loop() {
  data = analogRead(INPUTPIN);
  Serial.print(data);
  analogWrite(OUTPUTPIN, data);
  delay(20);
}

int data;
int INPUT_PIN = A0;
int OUTPUT_PIN = 6;

void setup() {
  Serial.begin(9600);
  while(Serial.read() != (byte)'0');
}


void loop() {
  data = analogRead(INPUT_PIN);
  delay(50);
}

void serialEvent() {
  char c;
  if(Serial.available() > 0) {
    c = Serial.read();
    if(c==byte('d')) {
      Serial.println(data);
    }
  }
}

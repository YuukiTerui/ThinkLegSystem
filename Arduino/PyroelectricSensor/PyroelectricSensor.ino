int time = 0;
int data = 0;
int INPUT_PIN = A0;

void setup() {
  Serial.begin(9600);
  Serial.write(byte('0'));
  while(Serial.read() != (byte)'0');
}

void loop() {
  time = millis();
  data = analogRead(INPUT_PIN);
  String s = String(time);
  s += ",";
  s += String(data);
  s += ";";
  Serial.println(s);
  delay(20);
}
void serialEvent() {
  if(Serial.available() > 0) {
    char c = Serial.read();
    if(c == byte('0')) {
      cnt = 0;
    }
  }
}


/* stream
void loop() {
  data = analogRead(INPUT_PIN);
  cnt++;
  delay(10);
}

void serialEvent() {
  String s = String(cnt);
  s += ",";
  if(Serial.available() > 0) {
    char c = Serial.read();
    if(c == byte('d')) {
      s += String(data);
      Serial.println(s);
    } else if(c == byte('0')) {
      cnt = 0;
    }
  }
}
*/

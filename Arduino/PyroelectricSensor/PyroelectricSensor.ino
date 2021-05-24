int data = 0;
int cnt = 0;
int INPUT_PIN = A0;

void setup() {
  Serial.begin(9600);
  while(Serial.read() != (byte)'0');
}

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

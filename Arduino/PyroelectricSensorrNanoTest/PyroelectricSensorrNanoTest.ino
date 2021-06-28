
#define INPUT_PIN A0
#define LED_PIN 13
unsigned long time_ = 0;
unsigned long start_time = 0;
String data = "";
bool send_flag = false;


void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
  Serial.print("arduino is avairable\n");
}

String create_send_data() {
  String s = String(millis() - start_time);
  s += ",";
  s += String(analogRead(A0));
  s += ",";
  s += String(analogRead(A1));
  s += ",";
  s += String(analogRead(A2));
  s += ",";
  s += String(analogRead(A3));
  s += ",";
  s += String(analogRead(A4));
  s += ",";
  s += String(analogRead(A5));
  s += "\n";
  return s;
}

void send_data(String data) { 
  Serial.print(data);
}

void(* resetFunc) (void) = 0;

void loop() {
  serialEvent();
  if (send_flag) {
    data = create_send_data();
    send_data(data);
  }
  delay(20);
}
void serialEvent() {
  if(Serial.available() > 0) { // 内部でloop毎にSerial.available()>0の時呼ばれる関数なはずだから要らないのかもしれない．
    char c = Serial.read();
    switch (c) {
      case byte('0'):
        send_flag = false;
        digitalWrite(LED_PIN, LOW);
        break;
      case byte('1'):
        send_flag = true;
        start_time = millis();
        digitalWrite(LED_PIN, HIGH);
        break;
      // default:
      case byte('9'):
        resetFunc();
        break;
    }
  }
}

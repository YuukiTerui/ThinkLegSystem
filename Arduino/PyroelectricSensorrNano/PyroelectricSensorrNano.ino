
#define INPUT_PIN A0
#define LED_PIN 13
unsigned long time_ = 0;
unsigned long start_time = 0;
int data = 0;
boolean send_flag = false;


void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
  //while(Serial.available()) Serial.read();
  Serial.print("arduino is avairable\n");
}

void send_data() {
  time_ = millis() - start_time;
  data = analogRead(INPUT_PIN);
  String s = String(time_);
  s += ",";
  s += String(data);
  s += '\n';
  Serial.print(s);
}

void(* resetFunc) (void) = 0;

void loop() {
  serialEvent();
  if (send_flag) {
    send_data();
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

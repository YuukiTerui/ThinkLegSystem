
#define INPUT_PIN A0

unsigned long time_ = 0;
int data = 0;
bool send_flag = false;


void setup() {
  Serial.begin(115200);
  while(Serial.available()) Serial.read();
  Serial.print("arduino is avairable\n");
}

void send_data() {
  time_ = millis();
  data = analogRead(INPUT_PIN);
  String s = String(time_);
  s += ",";
  s += String(data);
  s += '\n';
  Serial.print(s);
}

void(* resetFunc) (void) = 0;

void loop() {
  if (send_flag) {
    send_data();
  }
  delay(20);
}
void serialEvent() {
  if(Serial.available() > 0) { // 内部でloop毎にSerial.available()>0の時呼ばれる関数なはずだから要らないのかもしれない．
    char c = Serial.read();
    switch (c) {
      case '0':
        send_flag = false;
        break;
      case '1':
        send_flag = true;
        break;
      // default:
      case '9':
        resetFunc();
        break;
    }
  }
}

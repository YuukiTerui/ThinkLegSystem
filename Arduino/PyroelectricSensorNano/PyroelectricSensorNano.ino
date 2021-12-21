#define LED_PIN 13
unsigned long time_ = 0;
unsigned long start_time = 0;
unsigned long read_time = 0;
int interval = 10;
int v = 0;
int data = 1024 / 4; // TODO あとでセンサーの出力平均値に変更
boolean send_flag = false;

void(* resetFunc) (void) = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);
  Serial.print("arduino is avairable\n");
}


void read_v() {
  v = analogRead(A5);
}

int LPF(int y0, int raw) {
  float alpha = 0.7;
  float y;
  y = alpha * y0+ (1-alpha) * raw;
  return int(y);
}


void send_to_RPi(unsigned long t) {
  data = LPF(data, v);
  String s = String(t);
  s += ",";
  s += String(v);
  s += ",";
  s += String(data);
  s += '\n';
  Serial.print(s);
}

void loop() {
  serialEvent();
  read_v();
  int tmp_time = millis()-read_time;
  if (tmp_time >= interval) {
    time_ = tmp_time;
    if (send_flag) {
      send_to_RPi(time_);
    }
    read_time = millis();
  }
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

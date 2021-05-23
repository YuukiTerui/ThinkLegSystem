int data;
int INPUT_PIN = A0;
int OUTPUT_PIN = 6;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  data = analogRead(INPUT_PIN);
  Serial.println(data);
  analogWrite(OUTPUT_PIN, data); 
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}

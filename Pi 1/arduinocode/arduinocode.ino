int cb = 0; int cbPin = A0; int LED = 8; String kt1; int cbas = 0; int cbasPin = A1; int LEDtest = 4;

void setup() {
  Serial.begin(9600);pinMode(LED, OUTPUT); pinMode(cbPin,INPUT); pinMode(cbasPin, INPUT);
  pinMode(LEDtest, OUTPUT);
  Serial.setTimeout(10);
}

void loop() {

cb = analogRead(cbPin); cbas = analogRead(cbasPin);

if (cb > 300 and cbas > 300) {digitalWrite(LED, HIGH);}
else {digitalWrite(LED, LOW);}

if (cb > 300) { 
digitalWrite(LEDtest,HIGH);  
Serial.println("CO NGUOI");delay(10);
}
else { 
digitalWrite(LEDtest, LOW);
Serial.println("KHONG CO NGUOI");delay(10);
}
kt1 = "0";
while (kt1 == "0") {
if (Serial.available() > 0) { kt1 = Serial.readString(); kt1.trim(); /*Serial.println("reading");*/}}
//Serial.println(kt1);

}

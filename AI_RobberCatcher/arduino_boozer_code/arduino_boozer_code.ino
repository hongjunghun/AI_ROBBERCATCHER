void setup() {
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    String c = Serial.readStringUtil('\n');
    c.trim();
    
    if (c == "boozer!!"){
      tone(11, 440);
      delay(600);
      noTone(11);
      delay(500);
    }
  }
}

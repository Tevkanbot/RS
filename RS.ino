void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readString();  // str m15
    char command = input[0];             // char m
    input = input.substring(1);          // str 15
    int data = input.toInt();            // int 15
    Serial.println(command);
    Serial.println(data);
    if (command == 'm') {

      // Код для движения, data - место куда ехать, 0 - база, 1 - первое место и т.д.
    }

    if (command == 'b') {

      // Код для открытия ящика, data - открыть или закрыть, 0 - закрыть, 1 - открыть
    }

    if (command == 'i') {

      // Код для дисплея
    }

    if (command == 'p') {
      bool isPayDone = 0;
      // Код для работы с nfc, data - цена, в конце выводим сообщение об успешной или не успешной оплате
      if (isPayDone == true) Serial.println("PayConfirmed");
      else Serial.println("PayRejected");
    }
  }
}

#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

#define PN532_IRQ 9

SoftwareSerial mySerial(2, 3);  // RX, TX
Adafruit_PN532 nfc(PN532_IRQ, 100);
String displayStatus = "logo";

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.setTimeout(50);

  nfc.begin();
  int versiondata = nfc.getFirmwareVersion();
  nfc.SAMConfig();

  sendCommand("page logo");  //фикс дисплея, так как первую команду он игнорит
}

void sendCommand(const char *cmd) {
  mySerial.print(cmd);
  mySerial.write(0xFF);
  mySerial.write(0xFF);
  mySerial.write(0xFF);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readString();  // str m15
    input.trim();

    char command = input[0];     // char m
    input = input.substring(1);  // str 15

    if (command == 'm') {
      int data = input.toInt();  // int 15

      // Код для движения, data - место куда ехать, 0 - база, 1 - первое место и т.д.
    }

    if (command == 'b') {
      int data = input.toInt();  // int 15

      // Код для открытия ящика, data - открыть или закрыть, 0 - закрыть, 1 - открыть
    }

    if (command == 'd') {
      String potCommand = input.substring(4);
      input = input.substring(0, 4);
      if (input == "logo") {
        sendCommand("page logo");
        displayStatus = "logo";
      } else if (input == "face") {
        sendCommand("page face");
        displayStatus = "face";
      } else if (input == "payy") {
        sendCommand("page payy");
        displayStatus = "payy";
      } else if (input == "pays") {
        sendCommand("page pays");
        String command = "cost.txt=\"" + potCommand + "\"";
        sendCommand(command.c_str());
        //Serial.println("potCommand: " + potCommand);
        displayStatus = "pays";
      } else if (input == "shop") {
        if (displayStatus == "shop") {
          //Serial.println("potCommand: " + potCommand);

          if (potCommand == "tea") sendCommand("vis tea,1");               // Компонент tea на странице shop
          else if (potCommand == "bar") sendCommand("vis bar,1");          // Компонент bar на странице shop
          else if (potCommand == "coffee") sendCommand("vis coffee,1");    // Компонент coffee на странице shop
          else if (potCommand == "napkins") sendCommand("vis napkins,1");  /// Компонент napkins на странице shop
          else if (potCommand == "mask") sendCommand("vis mask,1");        // Компонент mask на странице shop
          else if (potCommand == "clear") sendCommand("page shop");
          else Serial.println("Неизвестный товар, попытка повторного включения shop или нескольто товариов в одной команде ");

        } else {
          sendCommand("page shop");
          displayStatus = "shop";
        }
      } else {
        Serial.println("Что за режим алё");
        sendCommand("page logo");
        displayStatus = "logo";
      }
      //Serial.println("DS: " + displayStatus);
    }

    if (command == 'p') {
      bool isPayDone = 0;

      uint8_t success;
      uint8_t uid[8];     // Буфер для хранения ID карты
      uint8_t uidLength;  // Размер буфера карты

      success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 20);
      if (success) isPayDone = 1;
      else Serial.println("PayRejected");
      //if (isPayDone == true) {
      //  Serial.println("PayConfirmed");
      //} else {
      //  Serial.println("PayRejected");
      //}
    }  // command p
  }    // if serial av
}  // loop

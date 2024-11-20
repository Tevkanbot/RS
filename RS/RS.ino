#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include "Servo.h"

#define PN532_IRQ 10

SoftwareSerial mySerial(2, 3);  // RX, TX
Adafruit_PN532 nfc(PN532_IRQ, 100);
String displayStatus = "logo";

Servo myservo; //сервопривод

// порты MotorShild
#define SPEED_1      5 
#define DIR_1        4
 
#define SPEED_2      6
#define DIR_2        7

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.setTimeout(50);

  nfc.begin();
  int versiondata = nfc.getFirmwareVersion();
  nfc.SAMConfig();

  myservo.attach(8); // сервопривод
  myservo.write(0); // сервопривод 

  for (int i = 4; i < 8; i++) {  //настройка портов MotorShild   
    pinMode(i, OUTPUT);
  }

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
      switch (data) {
        case 0:
          {
            //код для передвижения на базу
            digitalWrite(DIR_1, HIGH);
            digitalWrite(DIR_2, HIGH);
  
  // Включаем оба мотора на максимальной скорости
            analogWrite(SPEED_1, 150);
            analogWrite(SPEED_2, 150);
            delay(1000);
            analogWrite(SPEED_1, 0);
            analogWrite(SPEED_2, 0);
            Serial.println("Done");
            break;
          }
        case 1:
          {
            // код передвмжения на 1 место
              digitalWrite(DIR_1, LOW);
              digitalWrite(DIR_2, LOW);              
              
              analogWrite(SPEED_1, 150);
              analogWrite(SPEED_2, 150);
              delay(1000);
              analogWrite(SPEED_1, 0);
              analogWrite(SPEED_2, 0);
              Serial.println("Done");
            break;
          }
          case 2:
          {
            // код передвмжения на 2 место
              digitalWrite(DIR_1, LOW);
              digitalWrite(DIR_2, LOW);              
              
              analogWrite(SPEED_1, 150);
              analogWrite(SPEED_2, 150);
              delay(2000);
              analogWrite(SPEED_1, 0);
              analogWrite(SPEED_2, 0);
              Serial.println("Done");
            break;
          }
      }  //switch
      // Код для движения, data - место куда ехать, 0 - база, 1 - первое место и т.д.
    }

    if (command == 'b') {
      int data = input.toInt();  // int 15
      switch(data)
      {
        case 0:
        {
          myservo.write(0); 
          //закрытие ящика
          break;
        }
        case 1:
        {
          myservo.write(300); 
          //открытие ящика
          break;
        }
      }
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

      //success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 20);
      //if (success) Serial.println("PayCon
      //else Serial.println("PayRejected");
      delay(5000);
      Serial.println("PayConfirmed");
      //if (isPayDone == true) {
      //  Serial.println("PayConfirmed");
      //} else {
      //  Serial.println("PayRejected");
      //}
    }  // command p
    if (command == 'u') {
      // ТУТ ПИШЕШЬ НАХОЖДЕНИЕ РАСТОЯНИЯ
      // Serial.println(первое растояние, " ", второе расстояние);
      //Примеры выводов
      //105 143
      //83 180
    }
  }    // if serial av
}  // loop
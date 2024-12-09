#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include "Servo.h"

#define PN532_IRQ 13

SoftwareSerial mySerial(2, 3);  // RX, TX
Adafruit_PN532 nfc(PN532_IRQ, 100);
String displayStatus = "logo";

Servo myservo; //сервопривод

// порты MotorShild
#define SPEED_1      5 
#define DIR_1        4
 
#define SPEED_2      6
#define DIR_2        7

#define trigPin1 9 
#define echoPin1 10  // Пины для первого датчика
#define trigPin2 12
#define echoPin2 11  // Пины для второго датчика

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.setTimeout(50);

  nfc.begin();
  int versiondata = nfc.getFirmwareVersion();
  nfc.SAMConfig(); // Настройка модуля
  if (!versiondata) {
    Serial.println("Не удалось найти RFID/NFC сканер");
  }

  myservo.attach(8); // сервопривод
  myservo.write(0); // сервопривод 

  for (int i = 4; i < 8; i++) {  //настройка портов MotorShild   
    pinMode(i, OUTPUT);
  }

  sendCommand("page logo");  //фикс дисплея, так как первую команду он игнорит

  pinMode(trigPin1, OUTPUT); pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT); pinMode(echoPin2, INPUT);
}
int measureDistance(int trigPin, int echoPin) {
    digitalWrite(trigPin, LOW); 
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH); 
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    return pulseIn(echoPin, HIGH) * 0.034 / 2;
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
            digitalWrite(DIR_1, LOW);
            digitalWrite(DIR_2, LOW);
  
  // Включаем оба мотора на максимальной скорости
            analogWrite(SPEED_1, 255);
            analogWrite(SPEED_2, 255);
            delay(5000);
            break;
          }
        case 1:
          {
            // код передвмещения на 1 место
              digitalWrite(DIR_1, HIGH);
              digitalWrite(DIR_2, HIGH);              

              analogWrite(SPEED_1, 255);
              analogWrite(SPEED_2, 255);
              delay(5000);
            break;
          }
      }  //switch
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
          myservo.write(180); 
          //открытие ящика
          break;
        }
      }
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
        displayStatus = "pays";
      } else if (input == "shop") {
        if (displayStatus == "shop") {
          if (potCommand == "tea") sendCommand("vis tea,1");
          else if (potCommand == "bar") sendCommand("vis bar,1");
          else if (potCommand == "coffee") sendCommand("vis coffee,1");
          else if (potCommand == "napkins") sendCommand("vis napkins,1");
          else if (potCommand == "mask") sendCommand("vis mask,1");
          else if (potCommand == "clear") sendCommand("page shop");
          else Serial.println("Unknown product");
        } else {
          sendCommand("page shop");
          displayStatus = "shop";
        }
      } else {
        sendCommand("page logo");
        displayStatus = "logo";
      }
    }

    if (command == 'p') {
      while (true) {
        uint8_t success;
        uint8_t uid[8];     // Буфер для хранения ID карты
        uint8_t uidLength;  // Размер буфера карты

        // Ожидание карты
        success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 20);
        if (success) {
          Serial.println("PayConfirmed");
          break;
        }
        else{
          Serial.println("Notpaid");
        }
      }
    }

    if (command == 'u') {
        int distance1 = measureDistance(trigPin1, echoPin1);
        int distance2 = measureDistance(trigPin2, echoPin2);

        // Вывод расстояний с двух датчиков
        Serial.print((distance1 >= 2 && distance1 <= 400) ? distance1 : '-');
        Serial.print(" "); // Разделитель между значениями
        Serial.println((distance2 >= 2 && distance2 <= 400) ? distance2 : '-');
    }
  }
}
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include "Servo.h"
#include <Stepper.h>

#define PN532_IRQ 3  // Изменён порт подключения NFC на 3
// Используем аппаратный порт Serial3 для связи с Nextion (TX = 14, RX = 15)
#define nextion Serial3

// Параметры шагового двигателя
const int stepsPerRevolution = 200;   // Количество шагов за оборот
Stepper myStepper(stepsPerRevolution, 52, 50, 48, 46);

Adafruit_PN532 nfc(PN532_IRQ, 100);
String displayStatus = "logo";
Servo myservo;

// Структура для списка товаров
struct Product {
  String name;
  uint16_t price;
  uint16_t count;
};

// Единый список товаров (все категории)
Product products[] = {
  {"soup", 350, 0},
  {"fries", 250, 0},
  {"caesar", 310, 0},
  {"pilaf", 350, 0},
  {"borsch", 325, 0},
  {"pasta", 350, 0},
  {"tea", 85, 0},
  {"coffee", 130, 0},
  {"applejuice", 100, 0},
  {"morse", 100, 0},
  {"water", 60, 0},
  {"cola", 150, 0},
  {"sandwiches", 150, 0},
  {"saltedsticks", 100, 0},
  {"breadrolls", 70, 0},
  {"bagel", 90, 0},
  {"venus", 60, 0},
  {"jupiter", 60, 0},
  {"slippers", 50, 0},
  {"mask", 50, 0},
  {"pen", 50, 0},
  {"rs", 800, 0},
  {"glass", 1500, 0},
  {"train", 1000, 0}
};
const int productCount = sizeof(products) / sizeof(Product);

// Для хранения списка товаров, запрошенных дисплеем командой "p,<список>"
#define MAX_LAST_PRODUCTS 10
String lastProducts[MAX_LAST_PRODUCTS];
int lastProductsCount = 0;

int findProductIndex(String name) {
  for (int i = 0; i < productCount; i++) {
    if (products[i].name.equalsIgnoreCase(name)) {
      return i;
    }
  }
  return -1;
}

uint16_t calculateTotalCostUnified() {
  uint16_t total = 0;
  for (int i = 0; i < productCount; i++) {
    total += products[i].count * products[i].price;
  }
  return total;
}

void clearCart() {
  for (int i = 0; i < productCount; i++) {
    products[i].count = 0;
  }
  lastProductsCount = 0;
}

void sendCommand(String cmd) {
  nextion.print(cmd);
  nextion.write(0xFF);
  nextion.write(0xFF);
  nextion.write(0xFF);
}

void trimTrailingFF(String &s) {
  while (s.endsWith("\xFF")) {
    s.remove(s.length() - 1);
  }
}

String cleanInput(String s) {
  String result = "";
  for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c >= 32 && c <= 126) {
      result += c;
    }
  }
  return result;
}

void updateLastProductCounts() {
  for (int i = 0; i < lastProductsCount; i++) {
    int idx = findProductIndex(lastProducts[i]);
    uint16_t cnt = (idx != -1) ? products[idx].count : 0;
    sendCommand("count_" + String(i + 1) + ".txt=\"" + String(cnt) + "\"");
  }
  uint16_t totalCost = calculateTotalCostUnified();
  sendCommand("cost.txt=\"" + String(totalCost) + "\"");
}

void setup() {
  nextion.begin(9600);
  Serial.begin(9600);
  Serial.setTimeout(50);
  
  nfc.begin();
  int versiondata = nfc.getFirmwareVersion();
  nfc.SAMConfig();
  // Если NFC не найден, сообщение можно закомментировать
  if (!versiondata) { Serial.println("RFID/NFC scanner not found"); }
  
  myservo.attach(8);
  myservo.write(0);
  
  // Инициализация пинов для MotorShield
  for (int i = 4; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
  
  // Отладочные сообщения по дисплею можно отключить
  sendCommand("page logo");
}

void loop() {
  String input = "";
  String src = "";
  if (Serial.available() > 0) {
    input = Serial.readString();
    src = "PC";
  } else if (nextion.available() > 0) {
    input = nextion.readString();
    src = "Nextion";
  }
  Serial.println(src);
  Serial.println(input);
  if (input.length() > 0) {
    // Отладочные сообщения по дисплею отключены
    input.trim();
    input.replace("\xFF", "");
    input.replace("\r", "");
    input.replace("\n", "");
    trimTrailingFF(input);
    input = cleanInput(input);
    
    if (input.equals("dshop")) {
      sendCommand("page menu_main");
      lastProductsCount = 0;
    }
    else if (input.equals("dclear")) {
      clearCart();
    }
    else if (input.equalsIgnoreCase("n")) {
      uint8_t success;
      uint8_t uid[7];
      uint8_t uidLength;
      success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 1000);
      if (success) {
        String cardData = "n,";
        for (uint8_t i = 0; i < uidLength; i++) {
          if (uid[i] < 0x10) cardData += "0";
          cardData += String(uid[i], HEX);
        }
        cardData.toLowerCase();
        Serial.println(cardData);
      } else {
        Serial.println("n,NO_CARD");
      }
    }
    // Обработка команды оплаты "pay"
    else if (input.equalsIgnoreCase("pay")) {
      uint16_t totalCost = calculateTotalCostUnified();
      if (totalCost == 0) {
        return;
      }
      
      sendCommand("page payment_e");
      delay(500);
      sendCommand("bill.txt=\"" + String(totalCost) + "\"");
      
      // Ожидание NFC-карты в течение 30 секунд
      unsigned long startTime = millis();
      bool cardDetected = false;
      String cardUID = "";
      while (millis() - startTime < 30000) {
        uint8_t success;
        uint8_t uid[7];
        uint8_t uidLength;
        success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 500);
        if (success) {
          cardUID = "";
          for (uint8_t i = 0; i < uidLength; i++) {
            if (uid[i] < 0x10) cardUID += "0";
            cardUID += String(uid[i], HEX);
          }
          cardUID.toLowerCase();
          cardDetected = true;
          break;
        }
      }
      
      if (!cardDetected) {
        sendCommand("page animation");
        delay(5000);
        sendCommand("page payment_start");
      } else {
        // Если карта обнаружена, проверяем её UID.
        // Карты без денег: "08e9695b" и "2f10480f"
        if (cardUID.equals("08e9695b") || cardUID.equals("2f10480f")) {
          sendCommand("page stop_payment");
          delay(5000);
          sendCommand("page payment_start");
        } else {
          sendCommand("page payment_finally");
          delay(500);
          sendCommand("page great_payment");
          delay(5000);
          sendCommand("page face");
          // Формируем строку заказа: c,<totalCost>,<prod>,<prod>,...
          String cartInfo = "c," + String(totalCost);
          for (int i = 0; i < productCount; i++) {
            for (int j = 0; j < products[i].count; j++) {
              cartInfo += "," + products[i].name;
            }
          }
          Serial.println(cartInfo);
          clearCart();
        }
      }
    }
    // Обработка команды для обновления списка товаров "p,<список>"
    else if (input.startsWith("p")) {
      String params = input.substring(1);
      params.trim();
      if (params.length() == 0) {
        uint16_t totalCost = calculateTotalCostUnified();
        sendCommand("cost.txt=\"" + String(totalCost) + "\"");
      } else {
        if (params.charAt(0) == ',') {
          params = params.substring(1);
          params.trim();
        }
        lastProductsCount = 0;
        int start = 0;
        while (start < params.length() && lastProductsCount < MAX_LAST_PRODUCTS) {
          int commaIndex = params.indexOf(',', start);
          String token;
          if (commaIndex == -1) {
            token = params.substring(start);
            start = params.length();
          } else {
            token = params.substring(start, commaIndex);
            start = commaIndex + 1;
          }
          token.trim();
          if (token.length() > 0) {
            lastProducts[lastProductsCount++] = token;
          }
        }
        updateLastProductCounts();
      }
    }
    // Обработка команды для шагового двигателя "m"
    else if (input.startsWith("m")) {
      int steps = input.substring(1).toInt();
      myStepper.setSpeed(60);  // скорость 60 об/мин
      myStepper.step(steps);
    }
    else if (input.startsWith("b")) {
      int servoData = input.substring(1).toInt();
      if (servoData == 0)
        myservo.write(0);
      else if (servoData == 1)
        myservo.write(180);
    }
  }
}

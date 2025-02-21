#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include "Servo.h"

#define PN532_IRQ 13
// Используем аппаратный порт Serial3 для связи с Nextion (TX = 14, RX = 15)
#define nextion Serial3

Adafruit_PN532 nfc(PN532_IRQ, 100);
String displayStatus = "logo";
Servo myservo;

// Структура для единого списка товаров
struct Product {
  String name;
  uint16_t price;
  uint16_t count;
};

// Единый список всех товаров (из всех категорий)
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

// Функция поиска товара по имени; возвращает индекс или -1
int findProductIndex(String name) {
  for (int i = 0; i < productCount; i++) {
    if (products[i].name.equalsIgnoreCase(name)) {
      return i;
    }
  }
  return -1;
}

// Вычисление итоговой стоимости заказа
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

// Отправка команды на Nextion (автоматически добавляются три байта 0xFF)
void sendCommand(String cmd) {
  nextion.print(cmd);
  nextion.write(0xFF);
  nextion.write(0xFF);
  nextion.write(0xFF);
}

// Удаление завершающих байтов 0xFF
void trimTrailingFF(String &s) {
  while (s.endsWith("\xFF")) {
    s.remove(s.length() - 1);
  }
}

// Функция очистки строки от непечатных символов
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

// Обновление полей с количеством товаров для списка, запрошенного дисплеем
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
  if (!versiondata) {
    Serial.println("RFID/NFC scanner not found");
  }

  myservo.attach(8);
  myservo.write(0);

  for (int i = 4; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
  
  Serial.println("Robot");
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
  
  if (input.length() > 0) {
    Serial.println("Received from " + src + ": " + input);
    input.trim();
    input.replace("\xFF", "");
    input.replace("\r", "");
    input.replace("\n", "");
    trimTrailingFF(input);
    input = cleanInput(input);
    
    // Сначала проверяем команды, которые точно не начинаются с "p,"
    if (input.equals("dshop")) {
      sendCommand("page menu_main");
      lastProductsCount = 0;
    }
    else if (input.equals("dclear")) {
      clearCart();
      Serial.println("Cart cleared by external command dclear");
    }
    // Сначала проверяем, является ли команда оплатой "pay"
    else if (input.equalsIgnoreCase("pay")) {
      uint16_t totalCost = calculateTotalCostUnified();
      if (totalCost == 0) {
        Serial.println("Pay command ignored: cart is empty");
        return;
      }
      Serial.println("Calculated totalCost: " + String(totalCost));
      
      // Переключаем дисплей на страницу payment_e (где отображается bill.txt)
      sendCommand("page payment_e");
      delay(500);
      
      // Обновляем поле bill.txt с итоговой суммой
      sendCommand("bill.txt=\"" + String(totalCost) + "\"");
      Serial.println("Sent bill.txt update: " + String(totalCost));
      
      // Блокирующее ожидание подтверждения оплаты от ПК через Serial
      Serial.println("Awaiting payment confirmation from PC (true/false/exit)...");
      String pcResponse = "";
      while (Serial.available() == 0) {
        // Ждем ответа
      }
      pcResponse = Serial.readString();
      pcResponse.trim();
      pcResponse = cleanInput(pcResponse);
      Serial.println("PC response: " + pcResponse);
      
      // Переключаем дисплей на страницу payment_finally
      sendCommand("page payment_finally");
      delay(500);
      if (pcResponse.equalsIgnoreCase("true")) {
        // Формируем строку заказа в формате: c,<totalCost>,<prod>,<prod>,...
        String cartInfo = "c," + String(totalCost);
        for (int i = 0; i < productCount; i++) {
          for (int j = 0; j < products[i].count; j++) {
            cartInfo += "," + products[i].name;
          }
        }
        Serial.println(cartInfo);
        sendCommand("page great_payment");
        delay(5000);
        sendCommand("page face");
        clearCart();
      }
      else if (pcResponse.equalsIgnoreCase("exit")) {
        sendCommand("page menu_main");
      }
      else {
        sendCommand("page stop_payment");
        delay(5000);
        sendCommand("page payment_start");
      }
    }
    // Затем обрабатываем команды обновления списка товаров "p,<список>"
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
    // Обработка команд изменения количества товара "+<товар>" и "-<товар>"
    else if (input.startsWith("+") || input.startsWith("-")) {
      char op = input.charAt(0);
      String prodName = input.substring(1);
      prodName.trim();
      int idx = findProductIndex(prodName);
      if (idx != -1) {
        if (op == '+')
          products[idx].count++;
        else if (op == '-' && products[idx].count > 0)
          products[idx].count--;
      }
      if (lastProductsCount > 0) {
        updateLastProductCounts();
      }
    }
    else if (input.startsWith("m")) {
      // Управление моторами (не реализовано)
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

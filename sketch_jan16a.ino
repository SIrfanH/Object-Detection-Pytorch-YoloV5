#include <LiquidCrystal_I2C.h>
String x;
String x_prv = "0000";

int Li          = 16;
int Lii         = 0;
int Ri          = -1;
int Rii         = -1;


String text = "                ";

LiquidCrystal_I2C lcd(0x27, 16, 2); // Bu kodu kullanırken ekranda yazı çıkmaz ise 0x27 yerine 0x3f yazınız !!


  

void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
   lcd.begin();
  lcd.setCursor(0, 0); // İlk satırın başlangıç noktası

  lcd.setCursor(0, 0);
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.clear();
           lcd.setCursor(0, 0);
          lcd.print("   CDTP GR 47   ");   
}
void loop() {
  lcd.setCursor(0, 1);

 if (Serial.available())
 {
  x = Serial.readString(); // 101
 }
 else
 {
  x = x_prv;
 }
 

 if (x[0] == '1')
 {
        lcd.setCursor(0, 1);
        lcd.print(Scroll_LCD_Left("YOLDA HAYVAN"));
 }
 else if (x[1] == '1')
 {
        lcd.setCursor(0, 1);
        lcd.print(Scroll_LCD_Left("DURAN ARABA"));
 }
 else if (x[2] == '1')
 {
        lcd.setCursor(0, 1);
        lcd.print(Scroll_LCD_Left("TERS YONDE ARABA"));
 }
 else if (x[3] == '1')
 {
         lcd.setCursor(0, 1);
        lcd.print(Scroll_LCD_Left("YOLDA KAMYON"));
 }
 else
 {
           lcd.setCursor(0, 0);
          lcd.print("   CDTP GR 47   ");  
          lcd.setCursor(0, 1);
        lcd.print(Scroll_LCD_Left(" IYI YOLCULUKLAR "));
 }
  x_prv = x;
 delay(250);

 
}

String Scroll_LCD_Left(String StrDisplay) {
  String result;
  String StrProcess = "                " + StrDisplay + "                ";
  result = StrProcess.substring(Li, Lii);
  Li++;
  Lii++;
  if (Li > StrProcess.length()) {
    Li = 16;
    Lii = 0;
  }
  return result;
}

void Clear_Scroll_LCD_Left() {
  Li = 16;
  Lii = 0;
}
//----------------------------------
String Scroll_LCD_Right(String StrDisplay) {
  String result;
  String StrProcess = "                " + StrDisplay + "                ";
  if (Rii < 1) {
    Ri  = StrProcess.length();
    Rii = Ri - 16;
  }
  result = StrProcess.substring(Rii, Ri);
  Ri--;
  Rii--;
  return result;
}

void Clear_Scroll_LCD_Right() {
  Ri = -1;
  Rii = -1;
}

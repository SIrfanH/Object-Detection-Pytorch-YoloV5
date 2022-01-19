import time
from RPLCD import CharLCD
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

anomaly = 0

while True:

    # ANOMALİYİ TUTAN DEĞİŞKEN anomaly olsun
    # BİR HABERLEŞME PROTOKOLÜYLE INT TİPİNDEKİ anomaly DEĞİŞKENİNİ ALDIĞINI VARSAY.
    # HABERLEŞME PROTOKOLÜ BU KISIMDA OLACAK:
    if anomaly == 1:
        lcd.write_string(u"KOPEK VAR")
    elif anomaly == 2:
        lcd.write_string(u"TAS VAR")
    elif anomaly == 3:
        lcd.write_string(u"DUBA VAR")
    else:
        lcd.write_string(u"ANOMALİ YOK!")

    time.sleep(1)
    lcd.clear()
    time.sleep(1)
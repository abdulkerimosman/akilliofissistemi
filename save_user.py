#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD

db = mysql.connector.connect(
  host="localhost",
  user="kerim",
  passwd="4374",
  database="personeltakipsistemi"
)

cursor = db.cursor()

reader = SimpleMFRC522()


try:
  while True:
    lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
    lcd.message('Yeni kayit icin\nokut')
    print('Yeni kayit icin\nokut')
    id, text = reader.read()
    cursor.execute("SELECT id FROM users WHERE rfid_uid="+str(id))
    cursor.fetchone()
    if cursor.rowcount >= 1:
      lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
      lcd.message("Overwrite\nexisting user?")
      print("Overwrite\nexisting user?")
      overwrite = input("Overwite (Y/N)? ")

      if overwrite[0] == 'Y' or overwrite[0] == 'y':
        lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
        lcd.message("Overwriting user.")
        print('Over writing user.')
        time.sleep(1)
        sql_insert = "UPDATE users SET name = %s WHERE rfid_uid=%s"
      else:
        continue;
    else:
      sql_insert = "INSERT INTO users (name, rfid_uid) VALUES (%s, %s)"
    lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
    lcd.message('Yeni isim yaz')
    print('Yeni isim yaz')
    new_name = input("Isim: ")

    cursor.execute(sql_insert, (new_name, id))

    db.commit()

    lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
    lcd.message("kullanici " + new_name + "\nKaydedildi!")
    print("kullanici " + new_name + "\nKaydedildi!")
    time.sleep(2)
finally:
  GPIO.cleanup()

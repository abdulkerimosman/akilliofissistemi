#!/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD
import dht11

db = mysql.connector.connect(
  host="localhost",
  user="kerim",
  passwd="4374",
  database="personeltakipsistemi"
)

cursor = db.cursor()
reader = SimpleMFRC522()

lcd_columns = 16
lcd_rows = 2

instance = dht11.DHT11(pin=5)

try:
  while True:
    lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, lcd_columns, lcd_rows)  # Recreate LCD object
    result = instance.read()
    lcd.clear()
    lcd.set_cursor(0, 0)  # Set cursor to the first column of the first row
    #lcd.message('Place Card')
    lcd.message('Kartinizi Okutunuz\ndegC={:.1f}'.format(result.temperature) if result.is_valid else 'Place Card - N/A°C')
    
    try:
      id, text = reader.read()

      cursor.execute("SELECT id, name FROM users WHERE rfid_uid="+str(id))
      result = cursor.fetchone()

      time.sleep(1)  # Add delay before clearing the LCD
      lcd.clear()  # Clear the entire LCD
      lcd.set_cursor(0, 0)  # Set cursor to the first column of the first row
      lcd.message('Hos Geldiniz')  # Write 'Place Card' message again

      if cursor.rowcount >= 1:
        lcd.set_cursor(0, 1)  # Set cursor to the first column of the second row
        lcd.message(result[1])  # Display the user's name on the second row
        cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],))
        db.commit()
      else:
        lcd.set_cursor(0, 0)  # Set cursor to the first column of the first row
        lcd.message('Kullanici   ')
        lcd.set_cursor(0, 1)  # Set cursor to the first column of the second row
        lcd.message('Bulunamadi!')

      time.sleep(2)
    except Exception as e:
            # Handle exceptions related to card reading or database connection
            lcd.clear()
            lcd.set_cursor(0, 0)
            lcd.message('Error: {}'.format(str(e)))
            print(f'Error: {str(e)}')
except KeyboardInterrupt:
    pass

finally:
  GPIO.cleanup()

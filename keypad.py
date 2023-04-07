#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Tornike Lasuridze"
__copyright__ = "Copyright 2021 IT-Security"
__credits__ = ["Tornike Lasuridze"]
__version__ = "1.0.0"
__license__ = "MIT"
__maintainer__ = "Tornike Lasuridze"
__email__ = "t.lasuridze@gmail.com"
__status__ = "Development"
import requests,os
import socket
import RPi.GPIO as GPIO
#import rpi_gpio
#rpi_gpio.__file__
#'/usr/local/lib/python3.7/dist-packages/pad4pi/rpi_gpio.py'
#from pad4pi import rpi_gpio
from pad4pi import rpi_gpio
import drivers
#from opendoor import OpenDoor
import time
import sys
from datetime import datetime,timedelta
import mysql.connector

db = mysql.connector.connect(
host="localhost",
user="Lasuridze",
passwd="Lasuridze7",
database="Lasuridze"
)
database = db.cursor()
display = drivers.Lcd()
GPIO.setwarnings(False)    # Ignore warning for now

try:
    mcp = display
except:
    print("I2C Address Error !")
    exit(1)    

# Create LCD, passing in MCP GPIO adapter.
lcd = mcp
"""
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [5, 12, 13, 19]  # BCM numbering
COL_PINS = [16, 26, 20]  # BCM numbering
#16: 1,4,7,*
#26: 2,5,8,
#20: 3,6,9,# 

KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]
 
ROW_PINS = [5, 12, 13, 19]  # BCM numbering
COL_PINS = [12, 16, 20, 21]  # BCM numbering
"""



#******************************************#
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

COL_PINS = [17, 27, 22, 5] # BCM numbering
ROW_PINS = [23,24,25,16] # BCM numbering
EnteredApp=0
entered_pin = ""
correct_pin = "123456"

Presentcardtext = "Pleas Enter PIN"

# CleanUp the resources
def cleanup():
    global entered_pin
    print("Enter your PIN:")
    print("Press * to clear previous digit.")
    print("Press # to confirm.")
    lcd.lcd_clear()
    #lcd.lcd_display_string("Goodbye...",1)
    lcd.backlight = False
    #initialize_lcd()
    entered_pin = ""

# Check entered PIN code
def check_pin(key):
    global entered_pin, correct_pin,cursor,EnteredApp



    if len(entered_pin) == 6 or key == "#":
        try:
            database.execute("""SELECT * FROM numbers lEFT JOIN userlogs ON userlogs.Card_Number = numbers.CardNumber WHERE numbers.CardNumber = %(Cardids)s order by userlogs.id DESC  limit 1""",{'Cardids': entered_pin})
            result = database.fetchone()
            print(result)
            if result is not None:
                UserNumb=result[2]
                today =  datetime.now()
                
                print("Name: ",result[1])
                print("Number: ", UserNumb)
                print("welcome:",result[2])
                print("End_Date: ",result[6])
                print("Start data: ",result[5])
                #print("Start data Y M D: ",result[5].strftime('%Y-%m-%d'))
                
                
                if result[6] is None and result[5] is None or datetime.today().strftime('%Y-%m-%d') != result[5].strftime('%Y-%m-%d'):
                    print("Insert If")
                    database.execute("INSERT INTO userlogs (Card_Number,Enter_Date) VALUES (%s,%s)", (UserNumb,today) )
                    db.commit()
                elif result[5] is not None and result[6] is None and today > result[5] + timedelta(minutes=3):
                    print("Update IF")
                    #database.execute("UPDATE userlogs SET (End_Date) VALUES (%s) WHERE", (UserNumb,) )
                    database.execute ("UPDATE userlogs SET End_Date= '%s' WHERE Card_Number = '%s' AND DATE(userlogs.Enter_Date) = CURRENT_DATE() order by userlogs.id DESC limit 1" %(today,UserNumb))
                    #database.execute("INSERT INTO userlogs (Card_Number) VALUES (%s)", (UserNumb,) )
                    db.commit()
                #except:
                    #print ("Shecdomis codi:everyday", sys.exc_info()[1])
                else:
                    print("cadet 3 wutis shemdeg: ")
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome "+result[1],1)
                correct_pin_entered("Welcome "+result[1])
                db.commit()
            else:
                db.commit()
                incorrect_pin_entered()
                
        except:
            print ("Shecdomis codi:everyday", sys.exc_info()[1])
                
            
 



# Display info on corrected PIN code and exit
def correct_pin_entered(dispayText):
    lcd.lcd_clear()
    lcd.lcd_display_string(dispayText,1)
    lcd.lcd_display_string("Accepted PIN",2)
    print("PIN accepted. Access granted.")
    time.sleep(3)
    #OpenDoor()
    cleanup()
    lcd.lcd_clear()
    lcd.lcd_display_string(Presentcardtext,1)
   
     
    


# Construct the entered PIN code
def digit_entered(key):
    global entered_pin, correct_pin

    entered_pin += str(key)
    print(entered_pin)

    lcd.lcd_clear()
    lcd.lcd_display_string("PIN: " + entered_pin,1)
    lcd.lcd_display_string("# to confirm",2)
    check_pin(key)


# Display info on in-corrected PIN code and exit
def incorrect_pin_entered():
    lcd.lcd_clear()
    #lcd.lcd_display_string("Access denied",1)
    lcd.lcd_display_string("Incorrect PIN",1)

    print("Incorrect PIN. Access denied.")
    
    time.sleep(5)
    lcd.lcd_clear()
    cleanup()
 


# Initialize the I2C LCD 1602 Display
def initialize_lcd():
    lcd.lcd_display_string("AsyaSoftware",1)
    #lcd.lcd_display_string("Enter your PIN",2)
    #lcd.lcd_display_string("Press * to clear",3)


# Manage no PIN code key
def non_digit_entered(key):
    global entered_pin

    if key == "*" and len(entered_pin) > 0:
        entered_pin = entered_pin[:-1]

        lcd.lcd_clear()
        lcd.lcd_display_string("PIN: " + entered_pin,1)
        lcd.lcd_display_string("# to confirm",2)
        
        print(entered_pin)
    if key == "#" and len(entered_pin) > 0:
        check_pin(key)


# Press handler key
def key_pressed(key):
    try:
        int_key = int(key)
        if 0 <= int_key <= 9:
            digit_entered(key)
    except ValueError:
        non_digit_entered(key)

def KeyAccess():
    try:
        factory = rpi_gpio.KeypadFactory()
        keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

        keypad.registerKeyPressHandler(key_pressed)

        initialize_lcd()

        print("Enter your PIN:")
        print("Press * to clear previous digit.")
        print("Press # to confirm.")

        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nApplication stopped!")
        lcd.lcd_clear()
        lcd.lcd_display_string("Goodbye...",1)
        time.sleep(2)
        lcd.lcd_clear()
        GPIO.cleanup()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    
        
KeyAccess()


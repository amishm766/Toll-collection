#!usr/bin/python

# Date : 14 Aug,2018
# Author : Ankit Mishra
# contact me on amishm766@gmail.com

""" IOT based toll collection with RFID using Raspberry pi """

import os
import csv
import sys
import time
import serial
import datetime
import RPi.GPIO as GPIO

global bal, min_balance, port
min_balance = 30
output_file = "customer.csv"
input_file = "change.csv"


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class my_lcd:
    global LCD_WIDTH, LCD_CHR, LCD_CMD, LCD_LINE_1, LCD_LINE_2
    global LCD_LINE_3, LCD_LINE_4, E_PULSE, E_DELAY
    
    LCD_WIDTH, LCD_CHR, LCD_CMD = 20, True, False
    LCD_LINE_1, LCD_LINE_2, LCD_LINE_3, LCD_LINE_4 = 0x80, 0xC0, 0x94, 0xD4
    E_PULSE, E_DELAY = 0.0005, 0.0005
    
    def __init__(self, pin_rs, pin_e, pins_db):
        
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setup(self.pin_e, GPIO.OUT)  
        GPIO.setup(self.pin_rs, GPIO.OUT)  
        for pin in self.pins_db:  
            GPIO.setup(pin, GPIO.OUT)  
        self.lcd_init()
        self.lcd_clear()

    def lcd_init(self):
        global command
        
        command = [0x33, 0x32, 0x06, 0x0C, 0x01]
        for i in range(len(command)):
            self.lcd_byte(command[i], LCD_CMD)
        
        time.sleep(E_DELAY)
        self.lcd_string("LCD INITIALIZED....", LCD_LINE_1)
        time.sleep(1)

    def lcd_clear(self):

        self.lcd_byte(0x01, LCD_CMD)

    def lcd_byte(self, bits, mode):
        """ Send command to LCD """  
  
        time.sleep(0.0005)  
        bits = bin(bits)[2:].zfill(8)          
        GPIO.output(self.pin_rs, mode)  
  
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i], True)  
  
        self.lcd_toggle_enable()
        
        for pin in self.pins_db:  
            GPIO.output(pin, False)  
  
        for i in range(4, 8):  
            if bits[i] == "1":  
                GPIO.output(self.pins_db[::-1][i-4], True)  

        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(E_DELAY)
        GPIO.output(self.pin_e, True)
        time.sleep(E_PULSE)
        GPIO.output(self.pin_e, False)
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
         
        message = message.ljust(LCD_WIDTH, " ")
         
        self.lcd_byte(line, LCD_CMD)
         
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)


class csv_class():
    global names, codes, balance

    def __init__(self):
        print("creating csv object")

    def column(self, filename):
        global arr, names, codes, balance
        arr = []
        codes = []
        names = []
        balance = []        
        with open(filename) as f:            
            for row in f:
                arr = row.split(',')
                codes.append(arr[1])
                names.append(arr[0])
                balance.append(arr[2])
            #codes = tuple(codes)
            #names = tuple(names)
            return tuple(names), tuple(codes), balance

    def csv_write(self, filename, mode, column1, column2, column3):
        text = [column1, column2, column3]
        with open(filename, mode) as f: 
            writer = csv.writer(f, delimiter=",", lineterminator='\n')
            writer.writerow(text)

    def csv_read_column(self, filename, columnNo):
        col = []        
        with open(filename, 'rb') as infile:
            for row in infile:
                arr = row.split(",")
                col.append(arr[columnNo - 1])
            return col                                    
                    

class serial_device():
    global port
    if os.path.exists("/dev/ttyUSB0"):
        port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=2)    

    def __init__(self, purpose, device):
        self.purpose = purpose
        self.device = device
        print("{} is initialized for {}".format(self.device, self.purpose))

    def serial_read(self):
        rcv = port.read(12)
        time.sleep(0.25)
        return rcv

class check(csv_class):
    global i
    i = 0
    
    def __init__(self):
        print("checking the database")

    def find_index(self):
        #names, codes, balance = col.column(input_file)
        for i in range(len(codes)):
            if code == codes[i]:
                return i
                
    def check_balance(self):
        #names, codes, balance = self.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:
                print("your balance is {}".format(balance[i]))
                lcd.lcd_string("your balance is {}".format(balance[i]), LCD_LINE_2)
                return int(balance[i])

    def deduct_balance(self):        
        #names, codes, balance = col.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:
                tax = 20
                balance[i] = str(int(balance[i])-tax) + '\n'
                print("Rs. {} has been deducted from your account".format(tax))
                print("the new balance is {}".format(balance[i]))
                lcd.lcd_string("new balance : {}".format(balance[i]), LCD_LINE_3)
                col.csv_write(input_file, "w", "name", "tag", "balance")
                for j in range(1, len(codes)):
                    col.csv_write(input_file, "a", names[j], codes[j], balance[j][:-1])            

    def check_database(self):
        time_string = datetime.datetime.now()
        #names, codes, balance = col.column(input_file)
        #code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:                
                #col.csv_write(output_file, "w", "name", "tag", "crossing time")
                col.csv_write(output_file, "a", names[i], codes[i], time_string)
                print("hello {}".format(names[i]))
                lcd.lcd_string("hello {}".format(names[i]), LCD_LINE_1)
                value = 'True'
                return value
            else:
                pass
                #print("Match not found")

def main():
    global col, code
    while True:
        code = rfid.serial_read()
        if sec.check_database() :
            if (int(sec.check_balance()) > min_balance):
                lcd.lcd_string("Welcome", LCD_LINE_4)
                sec.deduct_balance()
                time.sleep(2)
                lcd.lcd_string("Happy Journey", LCD_LINE_4)
                time.sleep(4)
            else:
                print("insufficient fund")
                lcd.lcd_string("insufficient fund", LCD_LINE_4)
                time.sleep(4)
        else:
            print("Swipe the card")
            lcd.lcd_clear()
            lcd.lcd_string("Swipe the card", LCD_LINE_1)


if __name__ == '__main__':
    try:
        global col, code        
        rfid = serial_device('security', 'rfid')
        col = csv_class()
        sec = check()
        lcd = my_lcd(22, 11,[23, 10, 9, 25])
        col.column(input_file)
        print("INITIALIZED")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_string("good bye", LCD_LINE_1)
        time.sleep(1)
        lcd.lcd_clear()
        GPIO.cleanup()

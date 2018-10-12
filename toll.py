

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
import sqlite3
import datetime

global bal
bal = 0
output_file = "/home/pi/Documents/toll/files/checkin.csv"
input_file = "files/update.csv"

class csv_class:

    def __init__(self):
        print("creating csv object")

    def column(self, filename):
        arr = []
        codes = []
        names = []
        balance = []        
        with open(filename) as f:            
            for row in f:
                arr=row.split(',')
                codes.append(arr[1])
                names.append(arr[0])
                balance.append(arr[2])
            return names, codes, balance

    def csv_write(self, filename, mode, column1, column2, column3):
        text = [column1, column2, column3]
        with open(filename, mode) as f: 
            writer = csv.writer(f, delimiter = ",", lineterminator ='\n')
            writer.writerow(text)

    def csv_read_column(self, filename, columnNo):
        col = []        
        with open(filename, 'rb') as infile:
            for row in infile:
                arr = row.split(",")
                col.append(arr[columnNo - 1])
            return col                                    
                    

class serial_device():
    global port, codes
    if os.path.exists("/dev/ttyUSB0"):
        port = serial.Serial("/dev/ttyUSB0", baudrate = 9600)    

    def __init__(self, purpose, device):
        self.purpose = purpose
        self.device = device
        print("{} is initialized for {}".format(self.device, self.purpose))

    def serial_read(self):
        rcv = port.read(12)
        return rcv

    def check_balance(self):        
        time_string = datetime.datetime.now()
        if os.path.exists("/dev/ttyUSB0"):
            code = self.serial_read()

        names, codes, balance = col.column(input_file)
        print(balance)
        code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:
                tax = 20
                balance[i] = str(int(balance[i])-tax) + '\n'
                col.csv_write('change.csv', "w", "name", "tag", "balance")
                for j in range(1,len(codes)):
                    col.csv_write('change.csv', "a", names[j], codes[j], balance[j][:-1])            

    def check_rfid(self):
        time_string = datetime.datetime.now()
        if os.path.exists("/dev/ttyUSB0"):
            code = self.serial_read()

        names, codes, balance = col.column(input_file)
        code = 'B'
        for i in range(len(codes)):
            if code == codes[i]:                
                #col.csv_write(output_file, "w", "name", "tag", "crossing time")
                col.csv_write(output_file, "a", names[i], codes[i], time_string)
                print("hello {}".format(names[i]))
                return True
            else:
                pass
                #print("Match not found")

def main():
    global col, rfid
    rfid = serial_device('security','rfid')
    col = csv_class()

    #col.csv_write(output_file, "w", "name", "tag", "crossing time")
    #col.csv_write('change.csv', "w", "name", "tag", "balance")

    #col.csv_write(input_file, "w", "name", "tag", "balance")
    #col.csv_write(input_file, "a", "ankit", "A", "30")
    #col.csv_write(input_file, "a", "avinash", "B", "20")
    #col.csv_write(input_file, "a", "harsh", "C", "10")
    #codes,names=col.column(input_file)
    #codes = col.csv_read_column(input_file,  2)
    #names = col.csv_read_column(input_file,  1)
    #balance = col.csv_read_column(input_file,  3)
    #print (names)
    #print( codes)
    #print (balance)
    check = True
    while check:
        rfid.check_rfid()
        if rfid.check_rfid():
            rfid.check_balance()
        time.sleep(0.5)
        #check = False
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

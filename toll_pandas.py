# Date : 30 Aug,2018
# Author : Ankit Mishra
# Project heading : Smart toll collection system

""" This project aims at the automation in the toll collection system
    supporting the digitaliztion of society. It reduces the human
    efforts to minimum and maximizes the accuracy. The database of
    the customer is created (number of times visited, crossing time,
    etc).     
"""

#!/usr/bin/env python
import os
import sys
import time
import glob
import serial
import logging
import numpy as np
import pandas as pd
import datetime as dt
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

filename = '/home/pi/Toll-collection/change.csv'
write_filename = '/home/pi/Toll-collection/change.csv'
update_filename =  '/home/pi/Toll-collection/customer.csv'

class serial_device():
    """ This class contains information about the serial device (here RFID)
    """
    global port, rcv
    port_detect = glob.glob("/dev/ttyUSB*") or glob.glob("/dev/ttyAMA*")
    print(len(port_detect),"Ports detected")
    if (len(port_detect) != 0):				
        print("Ports detected is/are:")
        for i in range (0,len(port_detect)):
            print(port_detect[i])
        if (len(port_detect) == 1):
            port = serial.Serial(port_detect[0],baudrate=9600)
            print("connected to: {}".format(port_detect[0]))

        else:
            for i in range(0,len(port_detect)):
                print("Enter",i,"to connect to:",port_detect[i])
                y = int(input("Enter your choice of connection: "))
                while (y >= len(port_detect)):
                    print("Invalid choice")
                    for i in range(0,len(port_detect)):
                        print('Enter {} to select: {}'.format(i, detect_port[i]))
                    y = int(input('Enter your choice of connection'))
                port = serial.Serial(port_detect[y], baudrate=9600)
                print('Connected to: {}'.format(port_detect[y]))
                #return
       
    if os.path.exists("/dev/ttyUSB0"):
        port = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 2)    
        #logger.debug('Port found')
        
    def __init__(self, purpose, device):
        self.purpose = purpose
        self.device = device
        print("{} is initialized for {}".format(self.device, self.purpose))

    def __str__(self):
        print('rfid initialized')

    def serial_read(self):
        global rcv
        rcv = port.read(12)
        time.sleep(0.25)
        return str(rcv)

class search_database(serial_device):
    """This class contains the methods to search the words or a entire column or a row
    """    
    global foundIndex
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):        
            print("Opening File: {} to search into the database".format(self.filename))
        else:
            print("The file u want to open doesn't exists")
            
    def search_in_column(self, queryColumn):
        """ This method searches for the index of that word in column and returns that index
        """ 
        global data, foundIndex         
        data = pd.read_csv(filename)
        print(data)
        foundIndex = data[data[queryColumn] == word].index.tolist()
        print(foundIndex)
        print("the word: '{}' has been found at position'{}'".format(word, foundIndex[0]))
        return foundIndex[0]

    def search_in_rows(self,rows, word):
        """ This method searches for the index of that word in row and returns that index
        """
        
    def write_in_column(self, write_filename):
        data.to_csv(write_filename, index = False)

class customer(search_database):
    """ This class contains the customer related information
    """
    def __init__(self):
        print("customer object has been created")

    def checkin_status(self,update_filename):
        """ This method updates the checkins of customer to the status file
        """
        global checkStatus
        timeString = dt.datetime.now()
        checkStatus = pd.read_csv(update_filename)
        #checkStatus = update[['name', 'balance']].copy()
        checkStatus.iloc[foundIndex, 2] = timeString
        newCustomerBalance =  int(self.check_customer_balance())
        checkStatus.iloc[foundIndex, 1] = newCustomerBalance
        checkStatus.to_csv(update_filename, index = False)
        
    def check_user_name(self):
        """ This method returns the customer's name
        """
        customerName = data['name'].get_value(foundIndex[0])
        return customerName
        
    def check_customer_balance(self):
        """ This method returns the customer's balance
        """ 
        customerBalance = data['balance'].get_value(foundIndex[0])
        return customerBalance
    
    def deduct_balance(self):
        """ This method substracts the tax amount to be paid from the main balance
        """
        global newCustomerBalance
        tax = 30
        customerBalance =  int(self.check_customer_balance())
        if customerBalance > tax:
            newCustomerBalance = customerBalance - tax
            data.iloc[foundIndex[0],2] = newCustomerBalance
            print("Rs.20 has been deducted, new balance: {}".format(newCustomerBalance))
            return newCustomerBalance
        else:
            print("insufficient fund")
            customerBalance =  self.check_customer_balance()
            data.iloc[foundIndex[0],2] = customerBalance
            return customerBalance
        
    def customer_frequency(self):
        """ This method returns the number of times the customer has visited
        """
        global frequency
        checkStatus = pd.read_csv(update_filename)
        frequency = int(checkStatus['visiting frequency'].get_value(foundIndex[0]))
        #if frequency % 10  == 0:
        #    print("Thanks for visiting us!! {} you have visited here {} times".format(customerName, frequency))            
        checkStatus.iloc[foundIndex,3] = frequency + 1
        checkStatus.to_csv(update_filename, index = False)
        return frequency

def sms(username,password,message):
    q=way2sms.sms(username,password)
    q.send(mobile_number_to_send,message)
    n=q.msgSentToday()
    q.logout()



# Define main function
def main():
    """ This is the main function to run the toll collection system
    """
    global word, customerName
    gatePin = 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gatePin , GPIO.OUT)
    while True:
        word = ser.serial_read()
        print(str(word)[2:-2])
        word = str(word)[2:-1]
        if word:
            search.search_in_column('tag')
            print(np.array(data.iloc[:, 2]))
            customerName = cus.check_user_name()
            customerBalance = cus.check_customer_balance()
            print("{} has rs. {}".format(customerName, customerBalance))
            cus.deduct_balance()
            search.write_in_column(write_filename)
            cus.checkin_status(update_filename)
            cus.customer_frequency()
            GPIO.output(gatePin, GPIO.HIGH)
            print("Thanks for visiting us!! Happy journey")
            
           

            checkStatus['visiting frequency'].plot(kind = 'hist')
            plt.xlabel('frequency') 
            plt.show()
            print(data)
        else:
            print("please swipe card")

def log_file():
    logger = logging.getLogger('Toll_logger')
    fh = logging.FileHandler('/home/pi/Toll-collection/Toll.log')
    fh.setLevel(logging.DEBUG)
    ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(ff)
    logger.addHandler(fh)
    logger.info('The program is starting...')
    

if __name__ == '__main__':
    try:
        global logger
        logger = logging.getLogger('Toll_logger')      
        fh = logging.FileHandler('Toll.log')
        fh.setLevel(logging.DEBUG)
        ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(ff)
        logger.addHandler(fh)
        logger.error('Starting program...')
        search = search_database(filename)
        ser = serial_device("toll","rfid")
        cus = customer()
        #ser.__str__()
        #str(ser)
        #log_file()
        main() 
    except FileNotFoundError as er:
        print("The file you wanted to open doesn't exist")
        logger.exception(er)
    except KeyboardInterrupt:
        print("keyboard interrupt occured...")
        logger.exception("keyboard interrupt occured...")
    except Exception as e:
        print(e)
        logger.exception(e)
    finally:
        print("Closing program...")
        GPIO.cleanup()
        logger.info('Exiting Program')

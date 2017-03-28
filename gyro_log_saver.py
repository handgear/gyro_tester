#!/usr/bin/python
#-*- coding:utf-8 -*-
import serial
import signal
import time
import sys
import csv

OUTPUT_RATE = 100 # daya output rate == OUTPUT_RATE in ms

def run():
    # serial = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200, timeout=10)
    serial = start_serial('/dev/cu.SLAB_USBtoUART', 115200)
    #serial port for BT
    # serial2 = start_serial('/dev/cu.HC-05-DevB', 9600)

    # save data in csv formet
    # name csv file by current time
    date_stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    with open('./'+ date_stamp + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # add index to the first row
        writer.writerow(['roll','pitch','yaw','velo_x','velo_y','velo_z','pos_x','pos_y','pos_z'])
        while True:

            data_set = [] # list for one data set (x,y,z axis)
            while True:

                read_chars = serial.read(1)
                if read_chars == '\n': # end of one data set
                    break;

                data_set.append(read_chars)

                # remove \r in the end
                if data_set[len(data_set)-1] == '\r':
                    data_set.pop()
                # remove * char in front
                if data_set[0] == '*':
                    data_set.pop()

            data_str = "".join(data_set)
            print data_str #print like 0.016   -0.034    1.043

            splited_data = data_str.split(",")
            print splited_data

            writer.writerow(splited_data)

    serial.close()

def start_serial(serial_port_name ,baudrate):
    ser = serial.Serial(serial_port_name, baudrate, timeout=10)

    need_reset = raw_input("need reset?(hit 'y' for reset): ")
    if need_reset == 'y':
        ser.write("<lf>\r\n")
        time.sleep(2)
        # change data output rate
        ser.write("<sor" + str(OUTPUT_RATE) + ">\r\n")
        time.sleep(2)
        print "setting..."
        # enable position output
        ser.write("<sod2>\r\n")
        time.sleep(2)
        print "setting..."
        # enable velocity output
        #<soa1> for accelator output
        ser.write("<soa4>\r\n")
        time.sleep(2)
        print "setting..."
        # Filter Tolerance Accelerometer value change
        ser.write("<sfta10>\r\n")
        time.sleep(2)
        print "done reset"

    # reset position data to 0,0,0
    ser.write("<posz>\r\n")
    time.sleep(2)

    return ser

if __name__ == '__main__':
    run()

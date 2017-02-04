#!/usr/bin/python
import serial

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200, timeout=10)
ser.write("sp=1000\r\n") #period time in ms
ser.write("ss=1\r\n") #read acc data


while True:


    data_set = [] #list for one data set (x,y,z axis)
    while True:

        read_chars = ser.read(1)
        if read_chars == '\n': #end of one data set
            break;
        data_set.append(read_chars)
        #remove \r in the end
        if data_set[len(data_set)-1] == '\r':
            data_set.pop()

    data_str = "".join(data_set)
    # print data_str #print like 0.016   -0.034    1.043

    splited_data = data_str.split(" ")
    # print splited_data

    #remove empty elements
    splited_data = list(filter(None, splited_data))
    print splited_data



'''
    need to do something with data_set
    will use queue to maintain fix amount of data set
    [[x,y,z],[x1,y1,z1],[x2,y2,z2],...]

    after intergrate acc data to make velocity and position data
    actualy you need to remove G acc first...but how?
'''



ser.close()


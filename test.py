#!/usr/bin/python
#-*- coding:utf-8 -*-
import serial

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200, timeout=10)
ser.write("sp=200\r\n") #period time in ms
ser.write("ss=1\r\n") #read acc data

velocity = [0.0,0.0,0.0]
position = [0.0,0.0,0.0]
is_first_data = False
first_data = [] #for calibration
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

    if 's' in data_set: #skip command echo from sensor ex. ss=1
        continue;

    data_str = "".join(data_set)
    # print data_str #print like 0.016   -0.034    1.043

    splited_data = data_str.split(" ")
    # print splited_data

    #remove empty elements
    splited_data = list(filter(None, splited_data))
    print "splited_data: " + str(splited_data)

    acc_data_f = []
    for i in splited_data:
        acc_data_f.append(float(i))

    print "acc_data_f: " + str(acc_data_f)
    #============after listed data=======================
    #============calc velocity & position================
    if is_first_data == False:
        first_data = acc_data_f
        is_first_data = True

    for i in range(3):
        velocity[i] = velocity[i] + (acc_data_f[i] - first_data[i])
    print "velocity x:%.2f y:%.2f z:%.2f" %(velocity[0], velocity[1], velocity[2])

    for i in range(3):
        position[i] = position[i] + velocity[i]

    print "position x:%.2f y:%.2f z:%.2f" %(position[0], position[1], position[2])

    '''
    need to do something with data_set
    will use queue to maintain fix amount of data set
    [[x,y,z],[x1,y1,z1],[x2,y2,z2],...]

    굳이 큐를 사용해야 할 이유가 있나?
    초기값으로 초기화(이후 가속도값에서 빼준다거나-음수의 경우는 어떻게?)

    변동값이 일정수준 이하일때는 누적시키지 않도록 할 것



    after intergrate acc data to make velocity and position data
    actualy you need to remove G acc first...but how?
    '''

    print ""

ser.close()


#!/usr/bin/env python
#
#oled_test.py
#Program to Format USB drives to FAT32
#LEDs for status
#OLED display shows last ran stats

import bakebit_oled as oled

oled.init() #initializes the OLED display

oled.clearDisplay() #clears the display
oled.setNormalDisplay() #Set display to normal mode (i.e non-inverse mode)
oled.setPageMode() #Set addressing mode to Page Mode

#The 1218x32 OLED display is divided into 4 pages of 128x8 pixels each

texts = [ "Hello World!", "This is a test", "of the OLED display", "on the BakeBit" ]

for i in range(4):
    oled.setTextXY(0,i) #Set the cursor to the 1st page, 1st column
    oled.putString(str(i) + " " + texts[i]) #Print the text on the OLED display


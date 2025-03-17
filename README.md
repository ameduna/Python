# USB FORMATER USING NANOPI NEO

## Introduction
I am making a program that will work on a NanoPi Neo that will format a USB drive when there is one inserted.
Board website https://wiki.friendlyelec.com/wiki/index.php/NanoPi_NEO
The NanoPi Neo will control 4 LED and have a 128x32 oled display.

## Installation steps 
Freshly formatted SD card using h3-XYZ-friendlycore-jammy-4.14-armhf-YYYYMMDD.img.gz
Install Bakebit and its dependencies (from install.sh)
````
git clone --depth=1 https://github.com/friendlyarm/BakeBit.git
````
````
sudo apt-get install i2c-tools libi2c-dev minicom git -y
sudo apt-get install python3 python3-dev python3-smbus python3-serial python3-rpi.gpio python3-psutil python3-pil -y
````
Install WiringPi
````
git clone --depth=1 https://github.com/friendlyarm/WiringNP.git
````
Cd into the created directory and run:
````
sudo ./build
````
Add user to i2c group
````
sudo adduser ${USER_NAME} i2c
````
There is a part to make the libraries global but it has not implemented. (May autostart a program on reboot)

Install mkfs.vfat
````
sudo apt-get install dosfstools
````

## Functionallity

Now that WiringPi and Bakebit are installed I can verifya everything is working by using gpio
````
gpio readall
````
````
 +-----+-----+----------+------+---+-NanoPi-NEO--+------+----------+-----+-----+
 | BCM | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | BCM |
 +-----+-----+----------+------+---+----++----+---+------+----------+-----+-----+
 |     |     |     3.3V |      |   |  1 || 2  |   |      | 5V       |     |     |
 |  12 |   8 |  GPIOA12 | ALT5 | 0 |  3 || 4  |   |      | 5V       |     |     |
 |  11 |   9 |  GPIOA11 | ALT5 | 0 |  5 || 6  |   |      | 0v       |     |     |
 | 203 |   7 |  GPIOG11 |  OFF | 0 |  7 || 8  | 0 | ALT5 | GPIOG6   | 15  | 198 |
 |     |     |       0v |      |   |  9 || 10 | 0 | ALT5 | GPIOG7   | 16  | 199 |
 |   0 |   0 |   GPIOA0 | ALT5 | 0 | 11 || 12 | 0 |  OUT | GPIOA6   | 1   | 6   |
 |   2 |   2 |   GPIOA2 |  OFF | 0 | 13 || 14 |   |      | 0v       |     |     |  
 |   3 |   3 |   GPIOA3 |  OFF | 0 | 15 || 16 | 0 |  OFF | GPIOG8   | 4   | 200 |
 |     |     |     3.3v |      |   | 17 || 18 | 0 |  OFF | GPIOG9   | 5   | 201 |
 |  64 |  12 |   GPIOC0 | ALT4 | 0 | 19 || 20 |   |      | 0v       |     |     |
 |  65 |  13 |   GPIOC1 | ALT4 | 0 | 21 || 22 | 0 | ALT5 | GPIOA1   | 6   | 1   |
 |  66 |  14 |   GPIOC2 | ALT4 | 0 | 23 || 24 | 1 |  OUT | GPIOC3   | 10  | 67  |
 +-----+-----+----------+------+---+----++----+---+------+----------+-----+-----+
 | BCM | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | BCM |

````
````
gpio i2cd
````
````
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
````

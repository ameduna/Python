import os
import time
import subprocess

# Pin definitions
RED_LED = 7
GREEN_LED = 3
YELLOW_LED = 2
BLUE_LED = 6

# Function to initialize GPIO pins
def init_gpio():
    os.system(f"gpio mode {RED_LED} out")
    os.system(f"gpio mode {GREEN_LED} out")
    os.system(f"gpio mode {YELLOW_LED} out")
    os.system(f"gpio mode {BLUE_LED} out")
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

# Function to set LED status
def set_led_status(red, green, yellow, blue):
    os.system(f"gpio write {RED_LED} {red}")
    os.system(f"gpio write {GREEN_LED} {green}")
    os.system(f"gpio write {YELLOW_LED} {yellow}")
    os.system(f"gpio write {BLUE_LED} {blue}")

# Function to get USB drive information
def get_usb_info(device):
    format = subprocess.check_output(f"lsblk -no FSTYPE {device}", shell=True).decode().strip()
    size = subprocess.check_output(f"lsblk -no SIZE {device}", shell=True).decode().strip()
    vendor = subprocess.check_output(f"lsblk -S | grep {os.path.basename(device)} | awk '{{print $3}}'", shell=True).decode().strip()
    print(f"USB drive detected: {device}")
    print(f"Format: {format}")
    print(f"Size: {size}")
    print(f"Vendor: {vendor}")
    return size

# Function to format USB drive to FAT32
def format_usb_drive(device):
    print(f"Formatting {device} to FAT32...")
    set_led_status(0, 0, 0, 1)
    os.system(f"sudo mkfs.vfat -I -F 32 {device}")
    print(f"Format complete: {device}")

# Function to check formatted size
def check_size(device, original_size):
    formatted_size = subprocess.check_output(f"lsblk -no SIZE {device}", shell=True).decode().strip()
    original_size_bytes = int(subprocess.check_output(f"numfmt --from=iec {original_size}", shell=True).decode().strip())
    formatted_size_bytes = int(subprocess.check_output(f"numfmt --from=iec {formatted_size}", shell=True).decode().strip())
    size_diff = original_size_bytes - formatted_size_bytes
    size_diff_percent = (size_diff / original_size_bytes) * 100
    if size_diff_percent > 15:
        print(f"Size check failed: original size = {original_size}, formatted size = {formatted_size}")
        set_led_status(1, 0, 0, 0)
        return False
    else:
        print(f"Size check passed: original size = {original_size}, formatted size = {formatted_size}")
        set_led_status(0, 1, 0, 0)
        return True

# Initialize GPIO pins
init_gpio()

# Monitor for USB drive insertion and removal
while True:
    set_led_status(0, 0, 1, 0)
    # List all connected USB drives
    usb_devices = subprocess.check_output("lsblk -S | grep usb | awk '{print $1}'", shell=True).decode().split()

    # Check for new USB devices
    for device in usb_devices:
        if not os.path.isfile(f"/tmp/usb_{device}"):
            open(f"/tmp/usb_{device}", 'a').close()
            original_size = get_usb_info(f"/dev/{device}")
            format_usb_drive(f"/dev/{device}")
            check_size(f"/dev/{device}", original_size)

    # Check for removed USB devices
    for file in os.listdir("/tmp"):
        if file.startswith("usb_"):
            device = file.replace("usb_", "")
            if device not in usb_devices:
                os.remove(f"/tmp/{file}")
                print(f"USB drive removed: /dev/{device}")

    # Wait for 5 seconds before checking again
    time.sleep(5)
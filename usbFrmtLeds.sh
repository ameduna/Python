#!/bin/bash

# Pin definitions
RED_LED=7
GREEN_LED=3
YELLOW_LED=2
BLUE_LED=6

# Function to initialize GPIO pins
init_gpio() {
    gpio mode $RED_LED out
    gpio mode $GREEN_LED out
    gpio mode $YELLOW_LED out
    gpio mode $BLUE_LED out
}

# Function to set LED status
set_led_status() {
    local red=$1
    local green=$2
    local yellow=$3
    local blue=$4
    gpio write $RED_LED $red
    gpio write $GREEN_LED $green
    gpio write $YELLOW_LED $yellow
    gpio write $BLUE_LED $blue
}

# Function to get USB drive information
get_usb_info() {
    local device=$1
    local format=$(lsblk -no FSTYPE $device)
    local size=$(lsblk -no SIZE $device)
    local vendor=$(lsblk -S | grep $(basename $device) | awk '{print $3}')
    echo "USB drive detected: $device"
    echo "Format: $format"
    echo "Size: $size"
    echo "Vendor: $vendor"
    echo $size
}

# Function to format USB drive to FAT32
format_usb_drive() {
    local device=$1
    echo "Formatting $device to FAT32..."
    set_led_status 0 0 0 1
    sudo mkfs.vfat -I -F 32 $device
    echo "Format complete: $device"
}

# Function to check formatted size
check_size() {
    local device=$1
    local original_size=$2
    local formatted_size=$(lsblk -no SIZE $device)
    local original_size_bytes=$(numfmt --from=iec $original_size)
    local formatted_size_bytes=$(numfmt --from=iec $formatted_size)
    local size_diff=$(echo "$original_size_bytes - $formatted_size_bytes" | bc)
    local size_diff_percent=$(echo "scale=2; ($size_diff / $original_size_bytes) * 100" | bc)
    if (( $(echo "$size_diff_percent > 15" | bc -l) )); then
        echo "Size check failed: original size = $original_size, formatted size = $formatted_size"
        set_led_status 1 0 0 0
        return 1
    else
        echo "Size check passed: original size = $original_size, formatted size = $formatted_size"
        set_led_status 0 1 0 0
        return 0
    fi
}

# Initialize GPIO pins
init_gpio

# Monitor for USB drive insertion and removal
while true; do
    set_led_status 0 0 1 0
    # List all connected USB drives
    usb_devices=$(lsblk -S | grep usb | awk '{print $1}')
    
    # Check for new USB devices
    for device in $usb_devices; do
        if [ ! -f "/tmp/usb_$device" ]; then
            touch "/tmp/usb_$device"
            original_size=$(get_usb_info "/dev/$device")
            format_usb_drive "/dev/$device"
            check_size "/dev/$device" "$original_size"
        fi
    done
    
    # Check for removed USB devices
    for file in /tmp/usb_*; do
        device=$(basename $file | sed 's/usb_//')
        if ! echo "$usb_devices" | grep -q "$device"; then
            rm -f "$file"
            echo "USB drive removed: /dev/$device"
        fi
    done
    
    # Wait for 5 seconds before checking again
    sleep 5
done
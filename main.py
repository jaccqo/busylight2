import usb.core
import usb.util

def busylight():
    # Vendor ID and Product ID of the Busylight device
    VENDOR_ID = 0x27BB
    PRODUCT_ID = 0x3BCA

    # Define command to turn the Busylight to green
    # Here, we construct a command to set green LED intensity to 100%
    # Adjust as needed based on the provided specification
    command = [
        0b00010000,  # Command byte: 0b00RRGGBB (RR=red, GG=green, BB=blue)
        0x01,        # Repeat: Execute this step once
        0x00,        # Red LED intensity: 0% (ignored for green)
        0xFF,        # Green LED intensity: 100%
        0x00,        # Blue LED intensity: 0% (ignored for green)
        0x00,        # ON time: 0.1 second steps (ignored for steady on)
        0x00,        # OFF time: 0.1 second steps (ignored for steady on)
        0x00         # Ringtone: No audio setting
    ]

    # Find the Busylight device
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if device is None:
        raise ValueError("Busylight device not found")

    # Set up USB communication
    device.set_configuration()

    # Send the command
    device.write(0x01, command)  # Endpoint address may vary, adjust as needed

    print("Busylight turned to green.")

def all_devices():
        # Find all USB devices
    devices = usb.core.find(find_all=True)

    # Look for the Busylight device
    for device in devices:
        print(device._serial_number)
        print(device.idProduct )



all_devices()
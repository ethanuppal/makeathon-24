import serial

serial = serial.Serial('/dev/ttyACM0', 9600)
    
def signal():
    # Send a signal to activate dispenser
    serial.write(b'1')

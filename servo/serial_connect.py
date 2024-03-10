import serial
import time

serial = serial.Serial('/dev/ttyACM0', 9600)

def to_bytes(x: int):
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

while True:
    # serial1.write(to_bytes(100))  # Write a hundred degree setpoint
    # print(to_bytes(100))
    # time.sleep(3)
    # serial1.write(to_bytes(0))  # 0 Degree setpoint
    # print(to_bytes(0))
    # time.sleep(3)

    serial.write(b'100')
    time.sleep(3)
    serial.write(b'0')
    time.sleep(3)
    

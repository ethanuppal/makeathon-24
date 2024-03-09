import RPi.GPIO as GPIO
import time

def start_power(power_pin):
    # Set the pin as an output
    GPIO.setup(power_pin, GPIO.OUT)

    # Set the pin to high (3.3V)
    GPIO.output(power_pin, GPIO.HIGH)

# Function to set angle of the servo
def set_angle(angle):
    duty_cycle = (angle / 180.0) * (duty_cycle_max - duty_cycle_min) + duty_cycle_min
    pwm.ChangeDutyCycle(duty_cycle)

# ------------------------- #

# Set pin numbers
power_pin = 40
control_pin = 37

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Start Power
start_power(power_pin)

# Set PWM parameters
frequency = 50  # Hz (typical for servos)
duty_cycle_min = 2.5  # Duty cycle for 0 degrees
duty_cycle_max = 12.5  # Duty cycle for 180 degrees

# Initialize PWM
GPIO.setup(control_pin, GPIO.OUT)
pwm = GPIO.PWM(control_pin, frequency)
pwm.start(0)

try:
    while True:
        # Move servo to 0 degrees
        set_angle(0)
        time.sleep(1)  # Wait for 1 second

        # Move servo to 90 degrees
        set_angle(90)
        time.sleep(1)  # Wait for 1 second

        # Move servo to 180 degrees
        set_angle(180)
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

# pwm.ChangeDutyCycle(10) # Tells the servo to turn to the left ( -90 deg position )
# time.sleep(2) # Tells the servo to Delay for 5sec

# pwm.stop()
# GPIO.cleanup()


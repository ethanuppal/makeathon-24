import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set pin numbers
control_pin = 40

# Set PWM parameters
frequency = 50  # Hz (typical for servos)
duty_cycle_min = 2.5  # Duty cycle for 0 degrees
duty_cycle_max = 12.5  # Duty cycle for 180 degrees

# Initialize PWM
GPIO.setup(control_pin, GPIO.OUT)
pwm = GPIO.PWM(control_pin, frequency)
pwm.start(0)

# Function to set angle of the servo
def set_angle(angle):
    duty_cycle = (angle / 180.0) * (duty_cycle_max - duty_cycle_min) + duty_cycle_min
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Allow time for servo to reach position

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

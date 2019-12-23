"""
File: chapter10/stepper.py

Controlling a bipolar stepper motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio

pi = pigpio.pi()

CHANNEL_1_ENABLE_GPIO = 18                                          # (1)
CHANNEL_2_ENABLE_GPIO = 16

INPUT_1A_GPIO = 23  # Blue Coil 1 Connected to 1Y                   # (2)
INPUT_2A_GPIO = 24  # Pink Coil 2  Connected to 2Y
INPUT_3A_GPIO = 20  # Yellow Coil 3 Connected to 3Y
INPUT_4A_GPIO = 21  # Orange Coil 4 Connected to 4Y

# Influences speed of motor.
# Too low a value and motor will not step
# or will step erratically.
STEP_DELAY_SECS = 0.005  # (3)

# Coil GPIOs as a list.
coil_gpios = [                                                      # (4)
    INPUT_1A_GPIO,
    INPUT_2A_GPIO,
    INPUT_3A_GPIO,
    INPUT_4A_GPIO
]

# Initialise each coil GPIO as OUTPUT.
for gpio in coil_gpios:                                             # (5)
    pi.set_mode(gpio, pigpio.OUTPUT)


def off():
    for gpio in coil_gpios:                                         # (6)
        pi.write(gpio, pigpio.HIGH)  # Coil off


off()  # All coils off.

# Enable Channels (always high)
pi.set_mode(CHANNEL_1_ENABLE_GPIO, pigpio.OUTPUT)  # (7)
pi.write(CHANNEL_1_ENABLE_GPIO, pigpio.HIGH)
pi.set_mode(CHANNEL_2_ENABLE_GPIO, pigpio.OUTPUT)
pi.write(CHANNEL_2_ENABLE_GPIO, pigpio.HIGH)

# Half step sequence, 4096 steps per full rotation.
COIL_HALF_SEQUENCE = [                                              # (8)
    [1, 0, 0, 1],
    [1, 0, 0, 0],  # (a)
    [1, 1, 0, 0],
    [0, 1, 0, 0],  # (b)
    [0, 1, 1, 0],
    [0, 0, 1, 0],  # (c)
    [0, 0, 1, 1],
    [0, 0, 0, 1]   # (d)
]

# Full step sequence, 2048 steps per full rotation.
COIL_FULL_SEQUENCE = [                                              # (9)
    [1, 0, 0, 0],  # (a)
    [0, 1, 0, 0],  # (b)
    [0, 0, 1, 0],  # (c)
    [0, 0, 0, 1]   # (d)
]

# Use half or full sequence (by default)?
coil_sequence = COIL_HALF_SEQUENCE


def rotate(steps=1, sequence=None):                                 # (10)
    """ Rotate number of steps
        use -steps to rotate in reverse """
    if sequence == None:
        sequence = COIL_HALF_SEQUENCE

    if steps < 0:                                                   # (11)
        # Reverse Sequence
        sequence = sequence[::-1]

    for step in range(abs(steps) // len(sequence)):                 # (12)
        # print("\nStep #{}".format(step+1))

        for gpio_states in sequence:                                # (13)
            # print("  {}".format(gpio_states))

            for i in range(len(gpio_states)):                       # (14)
                coil_gpio = coil_gpios[i]  # (14)
                high_or_low = gpio_states[i]
                # print("    GPIO {} is {}".format(coil_gpio, high_or_low))
                pi.write(coil_gpio, high_or_low)                    # (15)

            # Delay after step.            
            sleep(STEP_DELAY_SECS)                                  # (16)

    off()  # Turn stepper coils off


if __name__ == '__main__':

    try:
        steps = 2048  # Steps for full 360 degree rotation.
        print("Full Sequence = {} steps for full 360 degree rotation.".format(steps))
        rotate(steps, COIL_FULL_SEQUENCE)
        rotate(-steps, COIL_FULL_SEQUENCE)
        sleep(1)

        steps *= 2  # * 2 since twice resolution for half stepping.
        print("Half Sequence = {} steps for full 360 degree rotation.".format(steps))
        rotate(steps, COIL_HALF_SEQUENCE)
        rotate(-steps, COIL_HALF_SEQUENCE)

    finally:
        off()  # Turn stepper coils off
        pi.stop()  # PiGPIO Cleanup

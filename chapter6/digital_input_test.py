"""
File: chapter6/digital_input_test.py

Test digital input.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
from time import sleep

GPIO_PIN=21
pi = pigpio.pi()
pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_OFF)
#pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_UP)
#pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_DOWN)

try:
    while True:
        state = pi.read(GPIO_PIN);
        print("GPIO {} is {}".format(GPIO_PIN, state))
        sleep(0.02)

except KeyboardInterrupt:
  print("Bye")
  pi.stop() # PiGPIO cleanup.
"""
  File: chapter1/gpio_pkg_check.py
  This Python 3 script checks for the availability of various Python GPIO Library Packages for the Raspberry Pi.
  It does this by attempting to import the Python package. If the package import is successful
  we report the package as Available, and if the import (or import initialization) fails for any reason,
  we report the package as Unavailable.
"""
try:
    import gpiozero
    print('GPIOZero   Available')
except:
    print('GPIOZero   Unavailable. Install with "pip install gpiozero"')

try:
    import pigpio
    print('PiGPIO    Available')
except:
    print('PiGPIO    Unavailable. Install with "pip install pigpio"')


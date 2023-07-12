from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED, Button

'''Declare host for remote GPIO Only use to control gpio remotely'''
# Declare host for remote GPIO
factory = PiGPIOFactory(host='192.168.0.102')

# Magnetic switch hold time
switch_hold_time = 3.0

# Pin definitions and initiate pin factory
solenoid_pin1 = 17
magSwitch_pin1 = 21

'''Pin definitions''' 

class SolenoidLock:
    solenoid_lock1 = LED(solenoid_pin1, initial_value=True, pin_factory=factory)
    
class MageneticSwitch:
    mag_switch1 = Button(magSwitch_pin1, pull_up=True, bounce_time=0.2, pin_factory=factory, hold_time=switch_hold_time)
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED, Button

'''Declare host for remote GPIO Only use to control gpio remotely'''

factory = PiGPIOFactory(host='192.168.0.102')

'''Pin definitions''' 
class SolenoidPins:
    solenoid_pin = LED(17, initial_value=True, pin_factory=factory)
    
class MageneticSwitchPins:
    mag_switch_pin = 21
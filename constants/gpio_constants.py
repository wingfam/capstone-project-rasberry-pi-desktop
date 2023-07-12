from hx711 import HX711
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED, Button

'''Declare host for remote GPIO Only use to control gpio remotely'''
factory = PiGPIOFactory(host='192.168.0.102')

# Magnetic switch hold time
switch_hold_time = 3.0

# Pin definitions and initiate pin factory
solenoid_pin_1 = 17
magSwitch_pin_1 = 21
loadcell_dout_1 = 23
loadcell_sck_1 = 24

# Loadcell reference unit
referenceUnit = 218

class SolenoidLock:
    solenoid_lock1 = LED(solenoid_pin_1, initial_value=True, pin_factory=factory)
    
class MageneticSwitch:
    mag_switch1 = Button(magSwitch_pin_1, pull_up=True, bounce_time=0.2, pin_factory=factory, hold_time=switch_hold_time)

class LoadCell:
    hx_1 = HX711(loadcell_dout_1, loadcell_sck_1)
    
    def __init__(self):
        self.hx_1.set_reading_format("MSB", "MSB")
        self.hx_1.set_reference_unit(referenceUnit)
        print("Loadcell init done!")
    
    def tare(self):
        self.hx_1.tare()
        print("Loadcell tare done!")      
    
    def powerUp(self):
        self.hx_1.power_up()
        print("Loadcell power up done!") 
        
    def powerDown(self):
        self.hx_1.power_down()
        print("Loadcell power down done!") 
        
    def reset(self):
        self.hx_1.reset()
        print("Loadcell reset done!") 
        
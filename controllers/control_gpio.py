import tkinter as tk
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory

from models.models import Box

# Declare host for remote GPIO
factory = PiGPIOFactory(host='192.168.0.102')

# Pin definitions and initiate pin factory
solenoid_pin = LED(17, initial_value=True, pin_factory=factory)
magSwitch_pin = Button(21, pull_up=True, bounce_time=0.2, pin_factory=factory, hold_time=1.5)

class CreateBoxController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def save(self, email):
        """
        Save the email
        :param email:
        :return:
        """
        try:
            # save the model
            self.model.email = email
            self.model.save()

            # show a success message
            self.view.show_success(f'The email {email} saved!')

        except ValueError as error:
            # show an error message
            self.view.show_error(error) 

class ControlPinController():
    def __init__(self, view):
        self.view = view
        
    # This gets called whenever the ON button is pressed
    def unlock_door(self):
        print("Box's door is unlocked")

        # Disable ON button, enable OFF button, and turn on LED
        self.view.button_on.config(state=tk.DISABLED, bg='gray64')
        self.view.button_off.config(state=tk.NORMAL, bg='gray99')
        solenoid_pin.off()

    # This gets called whenever the OFF button is pressed
    def lock_door(self):
        print("Box's door is locked")

        # Disable OFF button, enable ON button, and turn off LED
        self.view.button_on.config(state=tk.NORMAL, bg='gray99')
        self.view.button_off.config(state=tk.DISABLED, bg='gray64')
        solenoid_pin.on()

    def confirm(self):
        # Unlock box's door. Add wait for release event to magnetic switch
        # and check its state after 3 seconds
        self.unlock_door()
        isReleased = magSwitch_pin.wait_for_release(3.0)

        if not isReleased:
            print('Magnetic switch is released: ', isReleased)
            self.lock_door()
        else:
            # Add when held event to the switch. If the switch is held for
            # a hold_time seconds, activate lock_door function (check pin 
            # declare for hold_time)
            print("Add event to magnetic switch")
            magSwitch_pin.when_held = self.lock_door
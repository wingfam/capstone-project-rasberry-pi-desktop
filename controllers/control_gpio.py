import time
import tkinter as tk

check_weight_time = 3

class CreateBoxController():
    def __init__(self, model, view):
        self.model = model
        self.view = view

class ControlPinController():
    def __init__(self, model, view):
        self.view = view
        self.model = model
        
    # This gets called whenever the ON button is pressed
    def unlock_door(self):
        print("Box's door is unlocked")

        # Disable ON button, enable OFF button, and turn on LED
        self.view.button_on.config(state=tk.DISABLED, bg='gray64')
        self.view.button_off.config(state=tk.NORMAL, bg='gray99')
        
        self.model.solenoid.off()
        print(self.model.magSwitch.value)

    # This gets called whenever the OFF button is pressed
    def lock_door(self):
        print("Box's door is locked")

        # Disable OFF button, enable ON button, and turn off LED
        self.view.button_on.config(state=tk.NORMAL, bg='gray99')
        self.view.button_off.config(state=tk.DISABLED, bg='gray64')
        self.model.solenoid.on()
        print(self.model.magSwitch.value)
    
    def check_weight(self):
        count = 0
        weight_value = 0
        loadcell = self.model.loadcell
        
        # Loop check loadcell weight value every 3 seconds 
        while count < check_weight_time:
            weight_value = max(0, int(loadcell.get_weight(5)))
            print(weight_value)
            count += 1
            time.sleep(1)
            
        newText = str(weight_value) + " grams"
        self.view.weight_label.configure(text=newText)
        print("Check weight done!")

    def confirm(self):
        # Unlock box's door. Add wait for release event to magnetic switch
        # and check its state after 3 seconds
        self.unlock_door()
        isReleased = self.model.magSwitch.wait_for_release(3.0)

        if not isReleased:
            print('Magnetic switch is released: ', isReleased)
            self.lock_door()
        else:
            # Add when held event to the switch. If the switch is held for
            # a hold_time seconds, activate lock_door function (check pin 
            # declare for hold_time)
            print("Add event to magnetic switch")
            self.model.magSwitch.when_held = self.lock_door
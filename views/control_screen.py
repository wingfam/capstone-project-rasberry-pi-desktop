import customtkinter as ctk
import tkinter as tk
from tkinter import font

from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from controllers.control_gpio import ControlPinController

from models.models import Box

# Declare host for remote GPIO
factory = PiGPIOFactory(host='192.168.0.102')

# Pin definitions and initiate pin factory
solenoid_pin = LED(17, initial_value=True, pin_factory=factory)
magSwitch_pin = Button(21, pull_up=True, bounce_time=0.2, pin_factory=factory, hold_time=1.5)

class ControlPinScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.geometry("1024x600")
        self.title("Control Screen")
        self.controller = ControlPinController(view=self)
        
        # Create widgets
        button_font = font.Font(family='Helvetica', size=24, weight='bold')
        self.button_confirm = tk.Button(
            self, 
            text="CONFIRM", 
            width=10, 
            command=self.controller.confirm, 
            state=tk.NORMAL, 
            font=button_font, 
            bg='gray99'
        )
        self.button_on = tk.Button(
            self, text="ON", 
            width=10, 
            command=self.controller.unlock_door, 
            state=tk.NORMAL,
            font=button_font, 
            bg='gray99'
        )
        self.button_off = tk.Button(
            self, text="OFF", 
            width=10, 
            command=self.controller.lock_door, 
            state=tk.DISABLED, 
            font=button_font, 
            bg='gray64'
        )

        # Lay out widgets
        self.button_confirm.grid(row=0, column=0)
        self.button_on.grid(row=1, column=0)
        self.button_off.grid(row=2, column=0)
    
    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
import customtkinter as ctk
import tkinter as tk
from tkinter import font

from controllers.control_gpio import ControlPinController
from constants.gpio_constants import MageneticSwitch, SolenoidLock

from models.models import Box

class ControlPinScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        box1 = Box(SolenoidLock.solenoid_lock1, MageneticSwitch.mag_switch1)
        self.controller = ControlPinController(view=self, model=box1)
        
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
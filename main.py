import sys
import RPi.GPIO as GPIO
import customtkinter as ctk

from constants.gpio_constants import LoadCell, MageneticSwitch, SolenoidLock
from views.config_screen import ConfigScreen
from views.control_screen import ControlScreen
from views.main_screen import MainScreen
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen
from views.completion_screen import CompletionScreen
from views.instruction_screen import InstructionScreen
from views.pre_config_screen import PreConfigScreen

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.title("Smart Locker")
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.loadcell = LoadCell()
        self.loadcell.reset()
        self.loadcell.tare()
        
        self.app_data = {}
        
        self.box_model = {
            "Box1": {
                "nameBox": "01",
                "solenoid_lock": 0,
                "magnetic_switch": 0,
                "loadcell": 0,
            },
            "Box2": {
                "nameBox": "02",
                "solenoid_lock": SolenoidLock.solenoid_lock1,
                "magnetic_switch": MageneticSwitch.mag_switch1,
                "loadcell": LoadCell.hx_1,
            }
        }
        
        self.frames = {
            "MainScreen": MainScreen,
            "DeliveryScreen": DeliveryScreen,
            "PickupScreen": PickupScreen,
            "InstructionScreen": InstructionScreen,
            "CompletionScreen": CompletionScreen,
            "PreConfigScreen": PreConfigScreen,
            "ConfigScreen": ConfigScreen,
            "ControlPinScreen": ControlScreen,
        }
        
        for key, F in self.frames.items():
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MainScreen")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "CompletionScreen":
            frame.event_generate("<<GoBackMainScreen>>")
            frame.bind("<<GoBackMainScreen>>", frame.on_show_frame())


if __name__ == "__main__":
    root = MainApp()
    root.mainloop()

LoadCell().powerDown()
print("Cleaning...")
GPIO.cleanup()        
print("Bye!")
sys.exit()
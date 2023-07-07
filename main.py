import sys
import time
import signal 
# import RPi.GPIO as GPIO
# from gpiozero import LED, Button
import customtkinter as ctk

from constants.gpio_constants import Pin
from views.main_screen import MainScreen
from views.delivery_screen import DeliveryScreen
from views.pickup_screen import PickupScreen
from views.completion_screen import CompletionScreen
from views.instruction_screen import InstructionScreen

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.geometry("1024x600")
        self.title("Smart Locker")
        
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.app_data = {}
        
        self.frames = {
            "MainScreen": MainScreen,
            "DeliveryScreen": DeliveryScreen,
            "PickupScreen": PickupScreen,
            "InstructionScreen": InstructionScreen,
            "CompletionScreen": CompletionScreen,
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
                
    # Clean up when the user exits with keyboard interrupt
    # def cleanupSignal(self, signal): 
    #     GPIO.cleanup() 
    #     sys.exit(0)

    # Setup GPIO
    # def gpioSetup(self):
    #     # Use "GPIO" pin numbering
    #     GPIO.setmode(GPIO.BCM)

    #     # Set LED pin as output and turn it off by default
    #     GPIO.setup(Pin.solenoid_pin, GPIO.OUT)
    #     GPIO.output(Pin.solenoid_pin, GPIO.HIGH)

    #     # Set Reed Switch pin as input and pull down resistor
    #     GPIO.setup(Pin.mag_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #     # Set the cleanup handler for when user hits Ctrl-C to exit
    #     signal.signal(signal.SIGINT, self.cleanupSignal) 

if __name__ == "__main__":
    root = MainApp()
    root.mainloop()